from django.db import models
from django.forms import ValidationError
from django.core.exceptions import FieldError

# This is the place for storing global abstract models and things related to them
# No functioning models or local abstract models

# Currently base classes include: Soft Delete


class SoftDeleteManagerQuerySet(models.QuerySet):
    """ QuerySet for bulk operations on objects """

    def delete(self):
        super(SoftDeleteManagerQuerySet, self).update(active=False)

    def hard_delete(self):
        return super(SoftDeleteManagerQuerySet, self).delete()

    def active(self):
        return self.filter(active=True)

    def inactive(self):
        return self.exclude(active=True)


class SoftDeleteManager(models.Manager):
    """ Manager for BaseModel, must be inherited for each custom manager """

    def __init__(self, *args, **kwargs):
        self.active_only = kwargs.pop('active_only', True)
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.active_only:
            return SoftDeleteManagerQuerySet(self.model).active()
        return SoftDeleteManagerQuerySet(self.model)

    # Actually this may not be used at all, this method deletes all records in QuerySet
    def hard_delete_all(self):
        self.active_only = False
        return self.get_queryset().hard_delete()


class DBRelativeModel:
    """ Defines a lazy relation to a different model """

    def __init__(self, model, *, get_first=False, index=0, **lookups):
        if issubclass(model, models.Model):
            self.model = model
            self.lookups = lookups
            self.evaluated_models = set()
            self.get_first = get_first
            self.lookups_resolved = False
            self._instance_ = None
            self._related_models_ = set()

            if issubclass(model, BaseModel):
                self._instance_ = self.model.get_test_instances()
                if getattr(self._instance_, "__iter__", False):
                    if len(self._instance_) > index:
                        self._instance_ = self._instance_[index]
                    elif len(self._instance_) > 0:
                        self._instance_ = self._instance_[0]
                    else:
                        self._instance_ = None
                if self._instance_:
                    self._related_models_ = self._instance_.related_models
        else:
            raise RuntimeError("Model must be a subclass of %s" % models.Model.__qualname__)

    @property
    def related_models(self):
        return self._related_models_

    def resolve_lookups(self):
        if self.lookups_resolved:
            return

        for lookup in self.lookups:
            if isinstance(self.lookups[lookup], DBRelativeModel):
                relative_model = self.lookups[lookup]
                self.lookups[lookup] = relative_model.evaluate()
                self.evaluated_models = self.evaluated_models.union(relative_model.evaluated_models)

    def evaluate(self):
        if self._instance_:
            query = self.model.objects.filter(**self._instance_.data)

            if query.exists():
                self.evaluated_models = self.related_models
                self.evaluated_models.add(self.model)
                return query.first()

        if self.get_first or self.lookups or not self._instance_:
            self.resolve_lookups()
            query = self.model.objects.filter(**self.lookups)

            if query.exists():
                self.evaluated_models = self.related_models
                self.evaluated_models.add(self.model)
                return query.first()
            elif not self._instance_:
                raise RuntimeError("Can't evaluate model '%s': it's not a subclass of BaseModel and must be initialised"
                                   " manually")

        evaluated_instance = self._instance_.evaluate()

        self.evaluated_models = self._instance_.evaluated_models
        self.evaluated_models.add(self.model)

        return evaluated_instance


class DBTestModel:
    """ Defines a lazy model instance """

    def __init__(self, model, **data):
        if not issubclass(model, BaseModel):
            raise RuntimeError("Model must be a subclass of core.BaseModel")
        self.model = model
        self._data_ = data
        self._relations_resolved_ = False
        self.instance = None
        self._evaluated_models_ = set()
        self._related_models_ = set()

        for name, value in self._data_.items():
            if isinstance(value, DBRelativeModel):
                self._related_models_ = self._related_models_.union(value.related_models)

    def resolve_relations(self):
        if self._relations_resolved_:
            return

        for prop in self._data_.keys():
            if isinstance(self._data_[prop], DBRelativeModel):
                relative_model = self._data_[prop]
                self._data_[prop] = relative_model.evaluate()
                self._related_models_ = self._related_models_.union(relative_model.evaluated_models)

        self._relations_resolved_ = True

    @property
    def data(self):
        self.resolve_relations()
        return self._data_

    @property
    def related_models(self):
        return self._related_models_

    @property
    def evaluated_models(self):
        return self._evaluated_models_

    def evaluate(self):
        if self.instance:
            return self.instance

        try:
            query = self.model.objects.filter(**self.data)
        except FieldError as e:
            raise RuntimeError("Error while evaluating model '%s': %s: %s" %
                               (self.model.__name__, e.__class__.__qualname__, e))
        if query.exists():
            self.instance = query.first()
            self._evaluated_models_ = self.related_models
            self._evaluated_models_.add(self.model)
            print("%s: test object queried from database" % (self.model.__name__, ))
            return query.first()

        self.instance = self.model(**self.data)
        try:
            self.instance.save()
            self._evaluated_models_ = self.related_models
            self._evaluated_models_.add(self.model)
        except ValidationError as e:
            raise RuntimeError("Errors occurred when saving instance of model %s: %s" % (self.model.__name__, e))
        print("%s: created and saved test object" % self.model.__name__)
        return self.instance


class BaseModel(models.Model):
    """ Base class to provide soft deletion """

    id = models.BigAutoField(primary_key=True)

    active = models.BooleanField(default=True)

    objects = SoftDeleteManager()
    all_objects = SoftDeleteManager(active_only=False)

    validate = None
    pre_save = None

    class Meta:
        abstract = True

    @staticmethod
    def get_test_instances():
        """ Return DBTestModel instance or list of DBTestModel """
        raise NotImplementedError("Method get_test_instances in class $s is not implemented" % __class__)

    def delete(self, **kwargs):
        self.active = False
        self.save()

    def hard_delete(self, **kwargs):
        super(BaseModel, self).delete(**kwargs)

    def save(self, *args, ignore_validation=False, **kwargs):

        if not ignore_validation:
            try:
                self.full_clean()
            except ValidationError as e:
                raise e

        if self.validate and callable(self.validate) and not ignore_validation:
            self.validate()

        if self.pre_save and callable(self.pre_save):
            self.pre_save()

        super(BaseModel, self).save(*args, **kwargs)
