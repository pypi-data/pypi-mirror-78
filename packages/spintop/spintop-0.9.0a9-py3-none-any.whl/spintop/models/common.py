from typing import Optional
from collections.abc import Mapping

from .base import BaseDataClass

NO_VERSION = 'none'

class VersionIDRecord(BaseDataClass):
    id: Optional[str]
    version: Optional[str]
    
    @classmethod
    def create(cls, id_or_dict, version=None):
        if isinstance(id_or_dict, cls):
            return id_or_dict
        if isinstance(id_or_dict, Mapping):
            id = id_or_dict.get('id', None)
            version = id_or_dict.get('version', None)
        else:
            id = id_or_dict
            
        if version is None:
            version = NO_VERSION
            
        return cls(
            id=id,
            version=version
        )
        
    def match(self, other):
        id_match = self.id == other.id if self.id is not None else True
        version_match = self.version == other.version if self.version is not None else True
        return id_match and version_match

    def __str__(self):
        if self.version and self.version != NO_VERSION:
            return f'{self.id}-{self.version}'
        elif self.id:
            return str(self.id)
        else:
            return 'default'

TestbenchIDRecord = VersionIDRecord

DutIDRecord = VersionIDRecord

class OutcomeData(BaseDataClass):
    message: str = ''
    is_pass: bool = True
    is_skip: bool = False
    is_abort: bool = False
    is_ignore: bool = False
    
    def __bool__(self):
        return self.is_pass and not self.is_abort

    @classmethod
    def create(cls, outcome):
        if outcome is None:
            outcome = True
            
        if isinstance(outcome, cls):
            pass # already correct type
        elif isinstance(outcome, bool):
            outcome = cls(is_pass=outcome)
        elif isinstance(outcome, Mapping):
            outcome = cls(**outcome)
        else:
            raise TypeError((
    'Outcome (%s) should either be a boolean that indicates if this test passed or failed, ' 
    'or a dictionnary of one or more of the following attributes: %s'
            ) % (outcome, [f.name for f in cls.dataclass_fields()]))
        return outcome

    def impose_upon(self, other_outcome):
        if not self.is_ignore:
            # Pass propagates by falseness. False will propagate up, not True
            other_outcome.is_pass = other_outcome.is_pass and self.is_pass

            # Abort propagates by trueness. True will propagate up, not False
            other_outcome.is_abort = other_outcome.is_abort or self.is_abort

            # Abort propagates by trueness. True will propagate up, not False
            other_outcome.is_skip = other_outcome.is_skip or self.is_skip
