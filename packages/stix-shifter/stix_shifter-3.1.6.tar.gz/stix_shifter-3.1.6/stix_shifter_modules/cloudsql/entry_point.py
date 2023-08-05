from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
import json

class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        if connection:
            self.setup_transmission_simple(connection, configuration)