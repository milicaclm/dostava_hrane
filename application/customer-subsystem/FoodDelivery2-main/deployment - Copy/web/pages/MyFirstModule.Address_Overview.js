import { createElement } from "react";
const React = { createElement };

import { PageFragment } from "mendix/PageFragment";
import { ActionProperty } from "mendix/ActionProperty";
import { DatabaseObjectListProperty } from "mendix/DatabaseObjectListProperty";
import { ExpressionProperty } from "mendix/ExpressionProperty";
import { ListAttributeProperty } from "mendix/ListAttributeProperty";
import { SelectionProperty } from "mendix/SelectionProperty";
import { TemplatedWidgetProperty } from "mendix/TemplatedWidgetProperty";
import { TextProperty } from "mendix/TextProperty";
import { WebIconProperty } from "mendix/WebIconProperty";

import { ActionButton } from "mendix/widgets/web/ActionButton";
import { ConditionalVisibilityWrapper } from "mendix/widgets/web/ConditionalVisibilityWrapper";
import * as DatagridWidgetModule from "C:/Users/Korisnik/Mendix/FoodDelivery2-main/deployment/web/widgets/com/mendix/widget/web/datagrid/Datagrid.mjs";
const Datagrid = Object.getOwnPropertyDescriptor(DatagridWidgetModule, "Datagrid")?.value || Object.getOwnPropertyDescriptor(DatagridWidgetModule, "default")?.value;   
import * as DatagridNumberFilterWidgetModule from "C:/Users/Korisnik/Mendix/FoodDelivery2-main/deployment/web/widgets/com/mendix/widget/web/datagridnumberfilter/DatagridNumberFilter.mjs";
const DatagridNumberFilter = Object.getOwnPropertyDescriptor(DatagridNumberFilterWidgetModule, "DatagridNumberFilter")?.value || Object.getOwnPropertyDescriptor(DatagridNumberFilterWidgetModule, "default")?.value;   
import * as DatagridTextFilterWidgetModule from "C:/Users/Korisnik/Mendix/FoodDelivery2-main/deployment/web/widgets/com/mendix/widget/web/datagridtextfilter/DatagridTextFilter.mjs";
const DatagridTextFilter = Object.getOwnPropertyDescriptor(DatagridTextFilterWidgetModule, "DatagridTextFilter")?.value || Object.getOwnPropertyDescriptor(DatagridTextFilterWidgetModule, "default")?.value;   
import { Div } from "mendix/widgets/web/Div";
import { Text } from "mendix/widgets/web/Text";
import { addEnumerations, asPluginWidgets, t } from "mendix";

import { content as parentContent } from "../layouts/Atlas_Core.Atlas_Default.js";

const { $Div, $Text, $Datagrid, $DatagridTextFilter, $DatagridNumberFilter, $ConditionalVisibilityWrapper, $ActionButton } = asPluginWidgets({ Div, Text, Datagrid, DatagridTextFilter, DatagridNumberFilter, ConditionalVisibilityWrapper, ActionButton });

const region$Main = (historyId) => (<PageFragment renderKey={historyId}>{[
    <$Div key="p.MyFirstModule.Address_Overview.layoutGrid1"
        $widgetId="p.MyFirstModule.Address_Overview.layoutGrid1"
        class={"mx-name-layoutGrid1 mx-layoutgrid mx-layoutgrid-fluid container-fluid"}
        content={[
            <$Div key="p.MyFirstModule.Address_Overview.layoutGrid1$row0"
                $widgetId="p.MyFirstModule.Address_Overview.layoutGrid1$row0"
                class={"row"}
                content={[
                    <$Div key="p.MyFirstModule.Address_Overview.layoutGrid1$row0$column0"
                        $widgetId="p.MyFirstModule.Address_Overview.layoutGrid1$row0$column0"
                        class={"col-lg col-md col"}
                        content={[
                            <$Text key="p.MyFirstModule.Address_Overview.text1"
                                $widgetId="p.MyFirstModule.Address_Overview.text1"
                                class={"mx-name-text1"}
                                caption={ExpressionProperty({
                                    "expression": { "expr": { "type": "literal", "value": "Address" }, "args": {} }
                                })}
                                renderMode={"h2"} />,
                            <$Datagrid key="p.MyFirstModule.Address_Overview.dataGrid2_1"
                                $widgetId="p.MyFirstModule.Address_Overview.dataGrid2_1"
                                advanced={false}
                                datasource={DatabaseObjectListProperty({
                                    "dataSourceId": "p.0",
                                    "entity": "MyFirstModule.Address",
                                    "operationId": "WUC7p4R9DV+0oRBLZSr6sQ",
                                    "sort": []
                                })}
                                refreshInterval={0}
                                itemSelection={SelectionProperty({
                                    "selectionType": "Single",
                                    "dataSourceId": "p.0"
                                })}
                                itemSelectionMethod={"rowClick"}
                                itemSelectionMode={"clear"}
                                showSelectAllToggle={true}
                                loadingType={"spinner"}
                                columns={[
                                    {
                                        "showContentAs": "attribute",
                                        "attribute": ListAttributeProperty({
                                            "path": "",
                                            "entity": "MyFirstModule.Address",
                                            "attribute": "City",
                                            "attributeType": "String",
                                            "sortable": true,
                                            "filterable": true,
                                            "dataSourceId": "p.0",
                                            "isList": false
                                        }),
                                        "dynamicText": undefined,
                                        "exportValue": undefined,
                                        "header": ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "City" }, "args": {} }
                                        }),
                                        "tooltip": undefined,
                                        "filter": [
                                            <$DatagridTextFilter key="p.MyFirstModule.Address_Overview.textFilter2"
                                                $widgetId="p.MyFirstModule.Address_Overview.textFilter2"
                                                attrChoice={"auto"}
                                                attributes={[]}
                                                defaultFilter={"contains"}
                                                placeholder={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                })}
                                                adjustable={true}
                                                delay={500}
                                                screenReaderButtonCaption={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                })}
                                                screenReaderInputCaption={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "Search" }, "args": {} }
                                                })}
                                                class={"mx-name-textFilter2"} />
                                        ],
                                        "visible": ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": true }, "args": {} }
                                        }),
                                        "sortable": true,
                                        "resizable": true,
                                        "draggable": true,
                                        "hidable": "yes",
                                        "allowEventPropagation": true,
                                        "width": "autoFill",
                                        "minWidth": "auto",
                                        "minWidthLimit": 100,
                                        "size": 1,
                                        "alignment": "left",
                                        "wrapText": false
                                    },
                                    {
                                        "showContentAs": "attribute",
                                        "attribute": ListAttributeProperty({
                                            "path": "",
                                            "entity": "MyFirstModule.Address",
                                            "attribute": "Street",
                                            "attributeType": "String",
                                            "sortable": true,
                                            "filterable": true,
                                            "dataSourceId": "p.0",
                                            "isList": false
                                        }),
                                        "dynamicText": undefined,
                                        "exportValue": undefined,
                                        "header": ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "Street" }, "args": {} }
                                        }),
                                        "tooltip": undefined,
                                        "filter": [
                                            <$DatagridTextFilter key="p.MyFirstModule.Address_Overview.textFilter1"
                                                $widgetId="p.MyFirstModule.Address_Overview.textFilter1"
                                                attrChoice={"auto"}
                                                attributes={[]}
                                                defaultFilter={"contains"}
                                                placeholder={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                })}
                                                adjustable={true}
                                                delay={500}
                                                screenReaderButtonCaption={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                })}
                                                screenReaderInputCaption={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "Search" }, "args": {} }
                                                })}
                                                class={"mx-name-textFilter1"} />
                                        ],
                                        "visible": ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": true }, "args": {} }
                                        }),
                                        "sortable": true,
                                        "resizable": true,
                                        "draggable": true,
                                        "hidable": "yes",
                                        "allowEventPropagation": true,
                                        "width": "autoFill",
                                        "minWidth": "auto",
                                        "minWidthLimit": 100,
                                        "size": 1,
                                        "alignment": "left",
                                        "wrapText": false
                                    },
                                    {
                                        "showContentAs": "attribute",
                                        "attribute": ListAttributeProperty({
                                            "path": "",
                                            "entity": "MyFirstModule.Address",
                                            "attribute": "StreetNumber",
                                            "attributeType": "Integer",
                                            "sortable": true,
                                            "filterable": true,
                                            "dataSourceId": "p.0",
                                            "isList": false
                                        }),
                                        "dynamicText": undefined,
                                        "exportValue": undefined,
                                        "header": ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "Street number" }, "args": {} }
                                        }),
                                        "tooltip": undefined,
                                        "filter": [
                                            <$DatagridNumberFilter key="p.MyFirstModule.Address_Overview.numberFilter1"
                                                $widgetId="p.MyFirstModule.Address_Overview.numberFilter1"
                                                attrChoice={"auto"}
                                                attributes={[]}
                                                defaultFilter={"equal"}
                                                placeholder={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                })}
                                                adjustable={true}
                                                delay={500}
                                                screenReaderButtonCaption={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                })}
                                                screenReaderInputCaption={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "Search" }, "args": {} }
                                                })}
                                                class={"mx-name-numberFilter1"} />
                                        ],
                                        "visible": ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": true }, "args": {} }
                                        }),
                                        "sortable": true,
                                        "resizable": true,
                                        "draggable": true,
                                        "hidable": "yes",
                                        "allowEventPropagation": true,
                                        "width": "autoFill",
                                        "minWidth": "auto",
                                        "minWidthLimit": 100,
                                        "size": 1,
                                        "alignment": "right",
                                        "wrapText": false
                                    },
                                    {
                                        "showContentAs": "customContent",
                                        "attribute": ListAttributeProperty({
                                            "path": "",
                                            "entity": "MyFirstModule.Address",
                                            "attribute": "City",
                                            "attributeType": "String",
                                            "sortable": true,
                                            "filterable": true,
                                            "dataSourceId": "p.0",
                                            "isList": false
                                        }),
                                        "content": TemplatedWidgetProperty({
                                            "dataSourceId": "p.0",
                                            "editable": false,
                                            "children": () => [
                                                <$ConditionalVisibilityWrapper key="p.MyFirstModule.Address_Overview.actionButton2$visibility"
                                                    $widgetId="p.MyFirstModule.Address_Overview.actionButton2$visibility"
                                                    visible={ExpressionProperty({
                                                        "expression": { "expr": { "type": "function", "name": "_hasSomeRole", "parameters": [ { "type": "literal", "value": "Korisnik" } ] }, "args": {} }
                                                    })}
                                                    contents={[
                                                        <$ActionButton key="p.MyFirstModule.Address_Overview.actionButton2"
                                                            $widgetId="p.MyFirstModule.Address_Overview.actionButton2"
                                                            buttonId={"p.MyFirstModule.Address_Overview.actionButton2"}
                                                            class={"mx-name-actionButton2 btn-lg"}
                                                            renderType={"link"}
                                                            role={"button"}
                                                            buttonClass={"btn-primary"}
                                                            caption={ExpressionProperty({
                                                                "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                            })}
                                                            tooltip={TextProperty({
                                                                "value": ""
                                                            })}
                                                            icon={WebIconProperty({
                                                                "icon": { "type": "icon", "iconClass": "mx-icon-lined mx-icon-pencil" }
                                                            })}
                                                            action={ActionProperty({
                                                                "action": { "type": "openPage", "argMap": { "param$Address": { "widget": "p.MyFirstModule.Address_Overview.dataGrid2_1", "source": "object" } }, "config": { "name": "MyFirstModule/Address_NewEdit.page.xml", "location": "modal", "resizable": true, "allowedRoles": [ "Korisnik" ] }, "disabledDuringExecution": true },
                                                                "abortOnServerValidation": true
                                                            })} />
                                                    ]} />,
                                                <$ConditionalVisibilityWrapper key="p.MyFirstModule.Address_Overview.actionButton3$visibility"
                                                    $widgetId="p.MyFirstModule.Address_Overview.actionButton3$visibility"
                                                    visible={ExpressionProperty({
                                                        "expression": { "expr": { "type": "function", "name": "_hasSomeRole", "parameters": [] }, "args": {} }
                                                    })}
                                                    contents={[
                                                        <$ActionButton key="p.MyFirstModule.Address_Overview.actionButton3"
                                                            $widgetId="p.MyFirstModule.Address_Overview.actionButton3"
                                                            buttonId={"p.MyFirstModule.Address_Overview.actionButton3"}
                                                            class={"mx-name-actionButton3 btn-lg"}
                                                            renderType={"link"}
                                                            role={"button"}
                                                            buttonClass={"btn-primary"}
                                                            caption={ExpressionProperty({
                                                                "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                            })}
                                                            tooltip={TextProperty({
                                                                "value": ""
                                                            })}
                                                            icon={WebIconProperty({
                                                                "icon": { "type": "icon", "iconClass": "mx-icon-lined mx-icon-trash-can" }
                                                            })}
                                                            action={ActionProperty({
                                                                "action": { "type": "deleteObject", "argMap": { "$object": { "widget": "p.MyFirstModule.Address_Overview.dataGrid2_1", "source": "object" } }, "config": { "closePage": false, "operationId": "L1SuvBEKDF+FRjF93cs0gg" }, "disabledDuringExecution": true },
                                                                "abortOnServerValidation": true
                                                            })} />
                                                    ]} />
                                            ]
                                        }),
                                        "dynamicText": undefined,
                                        "exportValue": undefined,
                                        "header": ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                        }),
                                        "tooltip": undefined,
                                        "visible": ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": true }, "args": {} }
                                        }),
                                        "sortable": false,
                                        "resizable": true,
                                        "draggable": true,
                                        "hidable": "no",
                                        "allowEventPropagation": true,
                                        "width": "autoFit",
                                        "minWidth": "auto",
                                        "minWidthLimit": 100,
                                        "size": 1,
                                        "alignment": "left",
                                        "wrapText": false
                                    }
                                ]}
                                columnsFilterable={true}
                                pageSize={20}
                                pagination={"buttons"}
                                showPagingButtons={"always"}
                                showNumberOfRows={false}
                                pagingPosition={"bottom"}
                                loadMoreButtonCaption={ExpressionProperty({
                                    "expression": { "expr": { "type": "literal", "value": "Load More" }, "args": {} }
                                })}
                                showEmptyPlaceholder={"none"}
                                onClickTrigger={"double"}
                                filtersPlaceholder={[
                                    <$ConditionalVisibilityWrapper key="p.MyFirstModule.Address_Overview.actionButton1$visibility"
                                        $widgetId="p.MyFirstModule.Address_Overview.actionButton1$visibility"
                                        visible={ExpressionProperty({
                                            "expression": { "expr": { "type": "function", "name": "_hasSomeRole", "parameters": [] }, "args": {} }
                                        })}
                                        contents={[
                                            <$ActionButton key="p.MyFirstModule.Address_Overview.actionButton1"
                                                $widgetId="p.MyFirstModule.Address_Overview.actionButton1"
                                                buttonId={"p.MyFirstModule.Address_Overview.actionButton1"}
                                                class={"mx-name-actionButton1"}
                                                renderType={"button"}
                                                buttonClass={"btn-primary"}
                                                caption={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "New Address" }, "args": {} }
                                                })}
                                                tooltip={TextProperty({
                                                    "value": ""
                                                })}
                                                icon={WebIconProperty({
                                                    "icon": { "type": "icon", "iconClass": "mx-icon-lined mx-icon-add" }
                                                })}
                                                action={ActionProperty({
                                                    "action": { "type": "createObject", "argMap": {}, "config": { "entity": "MyFirstModule.Address", "operationId": "iJWEUBX+nVKI9+bw+V5Fvw", "pageSettings": { "name": "MyFirstModule/Address_NewEdit.page.xml", "location": "modal", "resizable": true, "allowedRoles": [ "Korisnik" ] }, "allowedRoles": [], "objectParameter": "param$Address" }, "disabledDuringExecution": true },
                                                    "abortOnServerValidation": true
                                                })} />
                                        ]} />
                                ]}
                                columnsSortable={true}
                                columnsResizable={true}
                                columnsDraggable={true}
                                columnsHidable={true}
                                configurationStorageType={"attribute"}
                                storeFiltersInPersonalization={true}
                                filterSectionTitle={ExpressionProperty({
                                    "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                })}
                                exportDialogLabel={ExpressionProperty({
                                    "expression": { "expr": { "type": "literal", "value": "Export progress" }, "args": {} }
                                })}
                                cancelExportLabel={ExpressionProperty({
                                    "expression": { "expr": { "type": "literal", "value": "Cancel data export" }, "args": {} }
                                })}
                                selectRowLabel={ExpressionProperty({
                                    "expression": { "expr": { "type": "literal", "value": "Select row" }, "args": {} }
                                })}
                                selectAllRowsLabel={ExpressionProperty({
                                    "expression": { "expr": { "type": "literal", "value": "Select all rows" }, "args": {} }
                                })}
                                class={"mx-name-dataGrid2_1"} />
                        ]} />
                ]} />
        ]} />
]}</PageFragment>);

export const title = t([
    "Address Overview"
]);

export const classes = "layout-atlas layout-atlas-responsive-default";

export const style = {};
export const content = { ...parentContent,
    "Atlas_Core.Atlas_Default.Main": region$Main,
};
