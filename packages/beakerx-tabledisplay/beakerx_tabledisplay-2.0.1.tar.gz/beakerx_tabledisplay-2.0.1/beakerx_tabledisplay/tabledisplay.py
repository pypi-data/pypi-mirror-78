# Copyright 2017 TWO SIGMA OPEN SOURCE, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import json
import numpy as np
import types
from beakerx_base import BaseObject, BeakerxDOMWidget
from ipykernel.comm import Comm
from jupyter_core import paths
from os import makedirs, path, fdopen, open as os_open, O_RDWR, O_CREAT
from pandas import DataFrame, RangeIndex, MultiIndex, DatetimeIndex
from traitlets import Unicode, Dict

from .tableitems import DateType, ColumnType, TableDisplayAlignmentProvider, TableDisplayStringFormat, Highlighter, \
    RowsToShow


class Table(BaseObject):
    NAT_VALUE = "NaT"
    PAGE_SIZE = 1000

    def __init__(self, *args, **kwargs):
        self.validate_args(args)
        self.values = []
        self.types = []
        types_map = dict()
        self.columnNames = []
        self.hasIndex = None
        if isinstance(args[0], DataFrame):
            self.convert_from_pandas(args, types_map)
        elif isinstance(args[0], dict):
            self.convert_from_dict(args)
        elif isinstance(args[0], list):
            self.convert_from_list(args, types_map)

        self.headersVertical = False
        self.headerFontSize = None
        self.contextMenuItems = []
        self.alignmentForType = {}
        self.tooManyRows = False
        self.stringFormatForColumn = {}
        self.subtype = "ListOfMaps"
        self.stringFormatForType = {}
        self.fontColor = []
        self.contextMenuTags = {}
        self.cellHighlighters = []
        self.type = "TableDisplay"
        self.timeZone = None
        if TableDisplay.timeZoneGlobal:
            self.timeZone = TableDisplay.timeZoneGlobal
        self.tooltips = []
        self.columnsFrozen = {}
        self.rendererForType = {}
        self.doubleClickTag = None
        self.alignmentForColumn = {}
        self.columnOrder = []
        self.rendererForColumn = {}
        self.dataFontSize = None
        self.columnsVisible = {}
        self.hasDoubleClickAction = False
        self.filteredValues = None
        self.startIndex = 0
        self.endIndex = Table.PAGE_SIZE
        self.loadingMode = 'ALL'
        self.rowsToShow = RowsToShow.SHOW_25
        self.auto_link_table_links = self.get_option("auto_link_table_links")
        self.show_publication = self.get_option("show_publication")

    def validate_args(self, args):
        if len(args) > 2 and len(args[1]) != len(args[2]):
            raise Exception("The length of types should be same as number of columns.")

    def convert_from_dict(self, args):
        self.columnNames.append("Key")
        self.columnNames.append("Value")
        for key in args[0].keys():
            row = [key, args[0].get(key, "")]
            self.values.append(row)

    def convert_from_list(self, args, types_map):
        for element in args[0]:
            for key in element.keys():
                if key not in self.columnNames:
                    self.columnNames.append(key)
                    column_type = self.convert_type(type(element[key]))
                    self.types.append(column_type)
                    types_map[key] = column_type
                elif types_map[key] != "string":
                    type_for_key = types_map[key]
                    column_type = self.convert_type(type(element[key]))
                    if type_for_key != column_type:
                        self.types[self.columnNames.index(key)] = "string"
                        types_map[key] = "string"
        for element in args[0]:
            row = []
            for columnName in self.columnNames:
                value = element.get(columnName, "")
                value_type = types_map.get(columnName)
                row.append(self.convert_value(value, value_type))
            self.values.append(row)

    @staticmethod
    def has_types(args):
        return len(args) > 2

    def convert_from_pandas(self, args, types_map):
        self.columnNames = args[0].columns.tolist()
        if args[0].index.name is not None and args[0].index.name in self.columnNames:
            self.columnNames.remove(args[0].index.name)

        if self.has_types(args):
            self.types = args[2]
            types_map = dict(zip(self.columnNames, self.types))
        else:
            column = None
            for column in self.columnNames:
                if column == "time":
                    column_type = "time"
                else:
                    column_type = self.convert_type(args[0].dtypes[column].name)
                self.types.append(column_type)
                types_map[column] = column_type
        for index in range(len(args[0])):
            row = []
            for columnName in self.columnNames:
                value = args[0][columnName].to_numpy()[index]
                value_type = types_map.get(columnName)
                row.append(self.convert_value(value, value_type))
            if not isinstance(args[0].index, RangeIndex):
                index_type = self.convert_type(args[0].index.dtype)
                index_values = args[0].index.to_numpy()[index]
                tz = self.get_tz(args[0].index)
                row[:0] = [self.convert_value(index_values, index_type, tz)]
            self.values.append(row)

        if not isinstance(args[0].index, RangeIndex) and column is not None:
            self.hasIndex = "true"
            if isinstance(args[0].index, MultiIndex):
                columns = list(map(lambda x: self.convert_none_to_index_name(x), args[0].index.names))
                self.columnNames[:0] = [', '.join(columns)]
            else:
                self.columnNames[:0] = [args[0].index.name]
            self.types[:0] = [self.convert_type(args[0].index.dtype)]

    @staticmethod
    def get_tz(index):
        if not isinstance(index, DatetimeIndex):
            return None
        tz = index.tz
        if tz is None:
            return None
        return tz.zone

    @staticmethod
    def convert_none_to_index_name(x):
        if x is None:
            return "index"
        else:
            return x

    @staticmethod
    def convert_value(value, value_type, tz=None):
        if value_type == "time":
            if isinstance(value, np.datetime64) and np.isnat(value):
                return str(Table.NAT_VALUE)
            return DateType(value, tz)
        else:
            return value

    @staticmethod
    def convert_type(object_type):
        type_name = str(object_type)
        if "float" in type_name:
            return "double"
        elif "int" in type_name:
            return "integer"
        elif "datetime" in type_name:
            return "time"
        elif "bool" in type_name:
            return "boolean"
        else:
            return "string"

    def setToolTip(self, configTooltip):
        for row_ind in range(0, len(self.values)):
            row = self.values[row_ind]
            rowToolTips = []
            for col_ind in range(0, len(row)):
                rowToolTips.append(configTooltip(row_ind, col_ind, self))
            self.tooltips.append(rowToolTips)

    def setDataFontSize(self, dataFontSize):
        self.dataFontSize = dataFontSize

    def setHeaderFontSize(self, headerFontSize):
        self.headerFontSize = headerFontSize

    def setFontColorProvider(self, colorProvider):
        self.startIndex = 0
        self.endIndex = Table.PAGE_SIZE
        self.fontColor = []
        for row_ind in range(0, len(self.values)):
            row = self.values[row_ind]
            row_font_colors = []
            for col_ind in range(0, len(row)):
                if self.is_not_index_column(col_ind):
                    row_font_colors.append(colorProvider(row_ind, col_ind, self))
            self.fontColor.append(row_font_colors)

    def is_not_index_column(self, col_ind):
        return not self.hasIndex or col_ind != 0

    def setHeadersVertical(self, headersVertical):
        self.headersVertical = headersVertical

    def setRowFilter(self, filter_row):
        self.filteredValues = []
        for row_ind in range(0, len(self.values)):
            if filter_row(row_ind, self.values):
                self.filteredValues.append(self.values[row_ind])

    def setRowsToShow(self, rows):
        self.rowsToShow = rows

    def transform(self):
        if TableDisplay.loadingMode == "ALL":
            return super(Table, self).transform()
        else:
            start_index = self.startIndex
            end_index = self.endIndex
            self_copy = copy.copy(self)
            i = 0
            newValues = []
            new_fonts = []
            has_next = len(self.values) > end_index
            while i < Table.PAGE_SIZE and has_next:
                currentValue = self.values[start_index]
                newValues.append(currentValue)
                has_next_font_color = len(self.fontColor) > end_index
                if has_next_font_color:
                    current_font = self.fontColor[start_index]
                    new_fonts.append(current_font)

                i = i + 1
                start_index = start_index + 1
            self_copy.values = newValues
            self_copy.fontColor = new_fonts
            self_copy.loadingMode = TableDisplay.loadingMode
            return super(Table, self_copy).transform()

    def transformWhenMoreRowsRequest(self):
        self.startIndex = self.endIndex
        self.endIndex = self.endIndex + Table.PAGE_SIZE
        return self.transform()

    @staticmethod
    def get_option(name):
        return TableSettings().load_options().get(name)


class TableDisplay(BeakerxDOMWidget):
    _view_name = Unicode('TableDisplayView').tag(sync=True)
    _model_name = Unicode('TableDisplayModel').tag(sync=True)
    _view_module = Unicode('beakerx_tabledisplay').tag(sync=True)
    _model_module = Unicode('beakerx_tabledisplay').tag(sync=True)
    _model_module_version = Unicode('*').tag(sync=True)
    _view_module_version = Unicode('*').tag(sync=True)

    loadingMode = 'ALL'
    timeZoneGlobal = None

    model = Dict().tag(sync=True)
    contextMenuListeners = dict()
    updateData = Dict().tag(sync=True)
    loadMoreRows = Unicode("loadMoreServerInit").tag(sync=True)

    def on_load_more_rows_change(self, change):
        if change.new == "loadMoreRequestJS":
            self.loadMoreRows = "loadMoreServerDone"
            self.updateData = self.chart.transformWhenMoreRowsRequest()

    def __init__(self, *args, **kwargs):
        super(TableDisplay, self).__init__(**kwargs)
        self.chart = Table(*args, **kwargs)
        self.model = self.chart.transform()
        self.on_msg(self.handle_msg)
        self.details = None
        self.observe(self.on_load_more_rows_change, names='loadMoreRows')

    def setAlignmentProviderForType(self, type, alignmentProvider):
        if isinstance(type, ColumnType):
            self.chart.alignmentForType[type.value] = alignmentProvider
            self.model = self.chart.transform()
        return self

    def setAlignmentProviderForColumn(self, column_name, display_alignment):
        if isinstance(display_alignment, TableDisplayAlignmentProvider):
            self.chart.alignmentForColumn[column_name] = display_alignment.value
        self.model = self.chart.transform()
        return self

    def setStringFormatForTimes(self, time_unit):
        self.setStringFormatForType(ColumnType.Time, TableDisplayStringFormat.getTimeFormat(time_unit))
        return self

    def setStringFormatForType(self, type, formater):
        if isinstance(type, ColumnType):
            self.chart.stringFormatForType[type.value] = formater
            self.model = self.chart.transform()
            return self

    def setStringFormatForColumn(self, column, formater):
        self.chart.stringFormatForColumn[column] = formater
        self.model = self.chart.transform()
        return self

    def setRendererForColumn(self, column, renderer):
        self.chart.rendererForColumn[column] = renderer
        self.model = self.chart.transform()
        return self

    def setRendererForType(self, type, renderer):
        if isinstance(type, ColumnType):
            self.chart.rendererForType[type.value] = renderer
            self.model = self.chart.transform()
        return self

    def setColumnFrozen(self, column, visible):
        self.chart.columnsFrozen[column] = visible
        self.model = self.chart.transform()
        return self

    def setColumnVisible(self, column, visible):
        self.chart.columnsVisible[column] = visible
        self.model = self.chart.transform()
        return self

    def setColumnOrder(self, order):
        self.chart.columnOrder = order
        self.model = self.chart.transform()
        return self

    def removeAllCellHighlighters(self):
        self.chart.cellHighlighters = []
        self.model = self.chart.transform()
        return self

    def addCellHighlighter(self, highlighter):
        if isinstance(highlighter, Highlighter):
            self.chart.cellHighlighters.append(highlighter)
            self.model = self.chart.transform()
        return self

    def setDoubleClickAction(self, listener):
        if listener is not None:
            if isinstance(listener, str):
                self.doubleClickListener = None
                self.chart.doubleClickTag = listener
            elif isinstance(listener, types.FunctionType):
                self.doubleClickListener = listener
                self.chart.doubleClickTag = None
                self.chart.hasDoubleClickAction = True

            self.model = self.chart.transform()

    def setTimeZone(self, timezone):
        self.chart.timeZone = timezone
        self.model = self.chart.transform()
        return self

    def addContextMenuItem(self, name, func):
        self.contextMenuListeners[name] = func
        self.chart.contextMenuItems.append(name)
        self.model = self.chart.transform()

    def doubleClickListener(self, row, column, tabledisplay):
        pass

    def handle_msg(self, tabledisplay, params, list):
        self.details = TableActionDetails(params)
        if 'params' in params:
            self._run_double_click_by_tag(params)
        elif 'event' in params:
            self._run_event(params, tabledisplay)

    def _run_event(self, params, tabledisplay):
        if params['event'] == 'DOUBLE_CLICK':
            self.doubleClickListener(params['row'], params['column'], tabledisplay)
            self.model = self.chart.transform()
        if params['event'] == 'CONTEXT_MENU_CLICK':
            func = self.contextMenuListeners.get(params['itemKey'])
            if func is not None:
                if isinstance(func, str):
                    self._run_by_tag(func)
                else:
                    func(params['row'], params['column'], tabledisplay)
                    self.model = self.chart.transform()

    def _run_double_click_by_tag(self, params):
        if params['params']['actionType'] == 'DOUBLE_CLICK' and self.chart.doubleClickTag is not None:
            self._run_by_tag(self.chart.doubleClickTag)

    def _run_by_tag(self, tag):
        arguments = dict(target_name='beakerx.tag.run')
        comm = Comm(**arguments)
        msg = {'runByTag': tag}
        state = {'state': msg}
        comm.send(data=state, buffers=[])

    def updateCell(self, row, columnName, value):
        row = self.chart.values[row]
        col_index = self.chart.columnNames.index(columnName)
        row[col_index] = value

    def sendModel(self):
        self.model = self.chart.transform()

    @property
    def values(self):
        return self.chart.values

    def setToolTip(self, configTooltip):
        self.chart.setToolTip(configTooltip)
        self.model = self.chart.transform()

    def setDataFontSize(self, dataFontSize):
        self.chart.setDataFontSize(dataFontSize)
        self.model = self.chart.transform()

    def setHeaderFontSize(self, headerFontSize):
        self.chart.setHeaderFontSize(headerFontSize)
        self.model = self.chart.transform()

    def setFontColorProvider(self, colorProvider):
        self.chart.setFontColorProvider(colorProvider)
        self.model = self.chart.transform()

    def setHeadersVertical(self, headersVertical):
        self.chart.setHeadersVertical(headersVertical)
        self.model = self.chart.transform()

    def setRowFilter(self, filter_row):
        self.chart.setRowFilter(filter_row)
        self.model = self.chart.transform()

    def setRowsToShow(self, rows):
        if isinstance(rows, RowsToShow):
            self.chart.setRowsToShow(rows)
            self.model = self.chart.transform()
        return self


class TableActionDetails:
    def __init__(self, params):
        if 'params' in params:
            self.row = params['params'].get('row')
            self.col = params['params'].get('col')
            self.contextMenuItem = params['params'].get('contextMenuItem')
            self.actionType = params['params'].get('actionType')
            self.tag = params['params'].get('tag')
        else:
            self.row = params.get('row')
            self.col = params.get('column')
            self.actionType = params.get('event')
            self.contextMenuItem = params.get('itemKey')
            self.tag = params.get('tag')

    def __str__(self):
        return '{} {} {} {}'.format(self.actionType, self.row, self.col, self.tag)


class TableSettings:

    def __init__(self):
        pass

    def save(self, content):
        makedirs(paths.jupyter_config_dir(), exist_ok=True)
        with fdopen(os_open(self.__config_path, O_RDWR | O_CREAT, 0o600), 'w+') as json_file:
            json_file.seek(0)
            json_file.truncate()
            json_file.write(
                json.dumps(self.__dict_merge(self.__default_config.copy(), content), indent=2, sort_keys=True))

    def load(self):
        try:
            json_file = open(self.__config_path)
            data = self.__dict_merge(self.__default_config, json.load(json_file))
        except:
            data = self.__default_config
            self.save(data)

        return data

    def load_options(self):
        return self.load().get('beakerx_tabledisplay').get('options')

    __default_config = {
        "beakerx_tabledisplay": {
            "version": 1,
            "options": {
                "auto_link_table_links": False,
                "show_publication": True
            }
        }
    }

    __config_path = path.join(paths.jupyter_config_dir(), 'beakerx_tabledisplay.json')

    def __dict_merge(self, target, *args):
        if len(args) > 1:
            for obj in args:
                self.__dict_merge(target, obj)
            return target
        obj = args[0]
        if not isinstance(obj, dict):
            return obj
        for k, v in obj.items():
            if k in target and isinstance(target[k], dict):
                self.__dict_merge(target[k], v)
            else:
                target[k] = copy.deepcopy(v)
        return target
