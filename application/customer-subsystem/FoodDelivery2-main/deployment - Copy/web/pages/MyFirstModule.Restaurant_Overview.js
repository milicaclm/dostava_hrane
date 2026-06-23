import { createElement } from "react";
const React = { createElement };

import { PageFragment } from "mendix/PageFragment";
import { ActionProperty } from "mendix/ActionProperty";
import { DatabaseObjectListProperty } from "mendix/DatabaseObjectListProperty";
import { ExpressionProperty } from "mendix/ExpressionProperty";
import { ListAttributeProperty } from "mendix/ListAttributeProperty";
import { TemplatedWidgetProperty } from "mendix/TemplatedWidgetProperty";
import { TextProperty } from "mendix/TextProperty";

import { ActionButton } from "mendix/widgets/web/ActionButton";
import { ConditionalVisibilityWrapper } from "mendix/widgets/web/ConditionalVisibilityWrapper";
import { Div } from "mendix/widgets/web/Div";
import { ListView } from "mendix/widgets/web/ListView";
import { Text } from "mendix/widgets/web/Text";
import { addEnumerations, asPluginWidgets, t } from "mendix";

import { content as parentContent } from "../layouts/Atlas_Core.Atlas_Default.js";

const { $Div, $Text, $ConditionalVisibilityWrapper, $ActionButton, $ListView } = asPluginWidgets({ Div, Text, ConditionalVisibilityWrapper, ActionButton, ListView });

const region$Main = (historyId) => (<PageFragment renderKey={historyId}>{[
    <$Div key="p.MyFirstModule.Restaurant_Overview.layoutGrid1"
        $widgetId="p.MyFirstModule.Restaurant_Overview.layoutGrid1"
        class={"mx-name-layoutGrid1 mx-layoutgrid mx-layoutgrid-fluid container-fluid"}
        content={[
            <$Div key="p.MyFirstModule.Restaurant_Overview.layoutGrid1$row0"
                $widgetId="p.MyFirstModule.Restaurant_Overview.layoutGrid1$row0"
                class={"row"}
                content={[
                    <$Div key="p.MyFirstModule.Restaurant_Overview.layoutGrid1$row0$column0"
                        $widgetId="p.MyFirstModule.Restaurant_Overview.layoutGrid1$row0$column0"
                        class={"col-lg col-md col"}
                        content={[
                            <$Text key="p.MyFirstModule.Restaurant_Overview.text1"
                                $widgetId="p.MyFirstModule.Restaurant_Overview.text1"
                                class={"mx-name-text1"}
                                caption={ExpressionProperty({
                                    "expression": { "expr": { "type": "literal", "value": "Restaurants" }, "args": {} }
                                })}
                                renderMode={"h2"} />,
                            <$ConditionalVisibilityWrapper key="p.MyFirstModule.Restaurant_Overview.actionButton1$visibility"
                                $widgetId="p.MyFirstModule.Restaurant_Overview.actionButton1$visibility"
                                visible={ExpressionProperty({
                                    "expression": { "expr": { "type": "function", "name": "_hasSomeRole", "parameters": [ { "type": "literal", "value": "Administrator" }, { "type": "literal", "value": "User" }, { "type": "literal", "value": "Korisnik" } ] }, "args": {} }
                                })}
                                contents={[
                                    <$ActionButton key="p.MyFirstModule.Restaurant_Overview.actionButton1"
                                        $widgetId="p.MyFirstModule.Restaurant_Overview.actionButton1"
                                        buttonId={"p.MyFirstModule.Restaurant_Overview.actionButton1"}
                                        class={"mx-name-actionButton1"}
                                        renderType={"button"}
                                        buttonClass={"btn-default"}
                                        caption={ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "MF Get restaurants2" }, "args": {} }
                                        })}
                                        tooltip={TextProperty({
                                            "value": ""
                                        })}
                                        action={ActionProperty({
                                            "action": { "type": "callMicroflow", "argMap": {}, "config": { "operationId": "MNrsC+IX4VqFL3e+S46alQ", "validate": "view", "allowedRoles": [ "Administrator", "User", "Korisnik" ] }, "disabledDuringExecution": true },
                                            "abortOnServerValidation": true
                                        })} />
                                ]} />,
                            <$ListView key="p.MyFirstModule.Restaurant_Overview.listView1"
                                $widgetId="p.MyFirstModule.Restaurant_Overview.listView1"
                                class={"mx-name-listView1"}
                                listValue={DatabaseObjectListProperty({
                                    "dataSourceId": "p.2",
                                    "entity": "MyFirstModule.RestaurantAPI",
                                    "operationId": "poC1fZUPY1KHw2ZI/KqzJg",
                                    "sort": []
                                })}
                                searchAttributes={[
                                    ListAttributeProperty({
                                        "path": "",
                                        "entity": "MyFirstModule.RestaurantAPI",
                                        "attribute": "name",
                                        "attributeType": "String",
                                        "sortable": true,
                                        "filterable": true,
                                        "dataSourceId": "p.2",
                                        "isList": false
                                    }),
                                    ListAttributeProperty({
                                        "path": "",
                                        "entity": "MyFirstModule.RestaurantAPI",
                                        "attribute": "address",
                                        "attributeType": "String",
                                        "sortable": true,
                                        "filterable": true,
                                        "dataSourceId": "p.2",
                                        "isList": false
                                    }),
                                    ListAttributeProperty({
                                        "path": "",
                                        "entity": "MyFirstModule.RestaurantAPI",
                                        "attribute": "phone",
                                        "attributeType": "String",
                                        "sortable": true,
                                        "filterable": true,
                                        "dataSourceId": "p.2",
                                        "isList": false
                                    }),
                                    ListAttributeProperty({
                                        "path": "",
                                        "entity": "MyFirstModule.RestaurantAPI",
                                        "attribute": "email",
                                        "attributeType": "String",
                                        "sortable": true,
                                        "filterable": true,
                                        "dataSourceId": "p.2",
                                        "isList": false
                                    }),
                                    ListAttributeProperty({
                                        "path": "",
                                        "entity": "MyFirstModule.RestaurantAPI",
                                        "attribute": "description",
                                        "attributeType": "String",
                                        "sortable": true,
                                        "filterable": true,
                                        "dataSourceId": "p.2",
                                        "isList": false
                                    }),
                                    ListAttributeProperty({
                                        "path": "",
                                        "entity": "MyFirstModule.RestaurantAPI",
                                        "attribute": "workingHours",
                                        "attributeType": "String",
                                        "sortable": true,
                                        "filterable": true,
                                        "dataSourceId": "p.2",
                                        "isList": false
                                    }),
                                    ListAttributeProperty({
                                        "path": "",
                                        "entity": "MyFirstModule.RestaurantAPI",
                                        "attribute": "unavailableReason",
                                        "attributeType": "String",
                                        "sortable": true,
                                        "filterable": true,
                                        "dataSourceId": "p.2",
                                        "isList": false
                                    }),
                                    ListAttributeProperty({
                                        "path": "",
                                        "entity": "MyFirstModule.RestaurantAPI",
                                        "attribute": "status",
                                        "attributeType": "String",
                                        "sortable": true,
                                        "filterable": true,
                                        "dataSourceId": "p.2",
                                        "isList": false
                                    }),
                                    ListAttributeProperty({
                                        "path": "",
                                        "entity": "MyFirstModule.RestaurantAPI",
                                        "attribute": "restaurantId",
                                        "attributeType": "String",
                                        "sortable": true,
                                        "filterable": true,
                                        "dataSourceId": "p.2",
                                        "isList": false
                                    }),
                                    ListAttributeProperty({
                                        "path": "",
                                        "entity": "MyFirstModule.RestaurantAPI",
                                        "attribute": "category",
                                        "attributeType": "String",
                                        "sortable": true,
                                        "filterable": true,
                                        "dataSourceId": "p.2",
                                        "isList": false
                                    }),
                                    ListAttributeProperty({
                                        "path": "",
                                        "entity": "MyFirstModule.RestaurantAPI",
                                        "attribute": "rating",
                                        "attributeType": "Decimal",
                                        "sortable": true,
                                        "filterable": true,
                                        "dataSourceId": "p.2",
                                        "isList": false
                                    }),
                                    ListAttributeProperty({
                                        "path": "",
                                        "entity": "MyFirstModule.RestaurantAPI",
                                        "attribute": "recommendationReason",
                                        "attributeType": "String",
                                        "sortable": true,
                                        "filterable": true,
                                        "dataSourceId": "p.2",
                                        "isList": false
                                    }),
                                    ListAttributeProperty({
                                        "path": "",
                                        "entity": "MyFirstModule.RestaurantAPI",
                                        "attribute": "recommendationScore",
                                        "attributeType": "Decimal",
                                        "sortable": true,
                                        "filterable": true,
                                        "dataSourceId": "p.2",
                                        "isList": false
                                    })
                                ]}
                                itemTemplate={TemplatedWidgetProperty({
                                    "dataSourceId": "p.2",
                                    "editable": false,
                                    "children": () => [
                                        <$Text key="p.MyFirstModule.Restaurant_Overview.text2"
                                            $widgetId="p.MyFirstModule.Restaurant_Overview.text2"
                                            class={"mx-name-text2"}
                                            caption={ExpressionProperty({
                                                "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "name" }, "args": { "currentObject": { "widget": "p.MyFirstModule.Restaurant_Overview.listView1", "source": "object" } } }
                                            })}
                                            renderMode={"h2"} />,
                                        <$Text key="p.MyFirstModule.Restaurant_Overview.text13"
                                            $widgetId="p.MyFirstModule.Restaurant_Overview.text13"
                                            class={"mx-name-text13"}
                                            caption={ExpressionProperty({
                                                "expression": { "expr": { "type": "function", "name": "_format", "parameters": [ { "type": "variable", "variable": "currentObject", "path": "rating" }, { "type": "literal", "value": "{\"decimalPrecision\":2}" } ] }, "args": { "currentObject": { "widget": "p.MyFirstModule.Restaurant_Overview.listView1", "source": "object" } } }
                                            })}
                                            renderMode={"h4"} />,
                                        <$ConditionalVisibilityWrapper key="p.MyFirstModule.Restaurant_Overview.text16$visibility"
                                            $widgetId="p.MyFirstModule.Restaurant_Overview.text16$visibility"
                                            visible={ExpressionProperty({
                                                "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "isRecommended" }, "args": { "currentObject": { "widget": "p.MyFirstModule.Restaurant_Overview.listView1", "source": "object" } } }
                                            })}
                                            contents={[
                                                <$Text key="p.MyFirstModule.Restaurant_Overview.text16"
                                                    $widgetId="p.MyFirstModule.Restaurant_Overview.text16"
                                                    class={"mx-name-text16"}
                                                    caption={ExpressionProperty({
                                                        "expression": { "expr": { "type": "function", "name": "_format", "parameters": [ { "type": "variable", "variable": "currentObject", "path": "isRecommended" }, { "type": "literal", "value": "{}" } ] }, "args": { "currentObject": { "widget": "p.MyFirstModule.Restaurant_Overview.listView1", "source": "object" } } }
                                                    })}
                                                    renderMode={"h4"} />
                                            ]} />,
                                        <$Text key="p.MyFirstModule.Restaurant_Overview.text3"
                                            $widgetId="p.MyFirstModule.Restaurant_Overview.text3"
                                            class={"mx-name-text3"}
                                            caption={ExpressionProperty({
                                                "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "address" }, "args": { "currentObject": { "widget": "p.MyFirstModule.Restaurant_Overview.listView1", "source": "object" } } }
                                            })}
                                            renderMode={"span"} />,
                                        <$Text key="p.MyFirstModule.Restaurant_Overview.text4"
                                            $widgetId="p.MyFirstModule.Restaurant_Overview.text4"
                                            class={"mx-name-text4"}
                                            caption={ExpressionProperty({
                                                "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "phone" }, "args": { "currentObject": { "widget": "p.MyFirstModule.Restaurant_Overview.listView1", "source": "object" } } }
                                            })}
                                            renderMode={"span"} />,
                                        <$Text key="p.MyFirstModule.Restaurant_Overview.text5"
                                            $widgetId="p.MyFirstModule.Restaurant_Overview.text5"
                                            class={"mx-name-text5"}
                                            caption={ExpressionProperty({
                                                "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "email" }, "args": { "currentObject": { "widget": "p.MyFirstModule.Restaurant_Overview.listView1", "source": "object" } } }
                                            })}
                                            renderMode={"span"} />,
                                        <$Text key="p.MyFirstModule.Restaurant_Overview.text6"
                                            $widgetId="p.MyFirstModule.Restaurant_Overview.text6"
                                            class={"mx-name-text6"}
                                            caption={ExpressionProperty({
                                                "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "description" }, "args": { "currentObject": { "widget": "p.MyFirstModule.Restaurant_Overview.listView1", "source": "object" } } }
                                            })}
                                            renderMode={"span"} />,
                                        <$Text key="p.MyFirstModule.Restaurant_Overview.text7"
                                            $widgetId="p.MyFirstModule.Restaurant_Overview.text7"
                                            class={"mx-name-text7"}
                                            caption={ExpressionProperty({
                                                "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "workingHours" }, "args": { "currentObject": { "widget": "p.MyFirstModule.Restaurant_Overview.listView1", "source": "object" } } }
                                            })}
                                            renderMode={"span"} />,
                                        <$Text key="p.MyFirstModule.Restaurant_Overview.text8"
                                            $widgetId="p.MyFirstModule.Restaurant_Overview.text8"
                                            class={"mx-name-text8"}
                                            caption={ExpressionProperty({
                                                "expression": { "expr": { "type": "function", "name": "_format", "parameters": [ { "type": "variable", "variable": "currentObject", "path": "acceptsOrders" }, { "type": "literal", "value": "{}" } ] }, "args": { "currentObject": { "widget": "p.MyFirstModule.Restaurant_Overview.listView1", "source": "object" } } }
                                            })}
                                            renderMode={"span"} />,
                                        <$ConditionalVisibilityWrapper key="p.MyFirstModule.Restaurant_Overview.text9$visibility"
                                            $widgetId="p.MyFirstModule.Restaurant_Overview.text9$visibility"
                                            visible={ExpressionProperty({
                                                "expression": { "expr": { "type": "function", "name": "not", "parameters": [ { "type": "variable", "variable": "currentObject", "path": "acceptsOrders" } ] }, "args": { "currentObject": { "widget": "p.MyFirstModule.Restaurant_Overview.listView1", "source": "object" } } }
                                            })}
                                            contents={[
                                                <$Text key="p.MyFirstModule.Restaurant_Overview.text9"
                                                    $widgetId="p.MyFirstModule.Restaurant_Overview.text9"
                                                    class={"mx-name-text9"}
                                                    caption={ExpressionProperty({
                                                        "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "unavailableReason" }, "args": { "currentObject": { "widget": "p.MyFirstModule.Restaurant_Overview.listView1", "source": "object" } } }
                                                    })}
                                                    renderMode={"span"} />
                                            ]} />,
                                        <$Text key="p.MyFirstModule.Restaurant_Overview.text10"
                                            $widgetId="p.MyFirstModule.Restaurant_Overview.text10"
                                            class={"mx-name-text10"}
                                            caption={ExpressionProperty({
                                                "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "status" }, "args": { "currentObject": { "widget": "p.MyFirstModule.Restaurant_Overview.listView1", "source": "object" } } }
                                            })}
                                            renderMode={"span"} />,
                                        <$Text key="p.MyFirstModule.Restaurant_Overview.text12"
                                            $widgetId="p.MyFirstModule.Restaurant_Overview.text12"
                                            class={"mx-name-text12"}
                                            caption={ExpressionProperty({
                                                "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "category" }, "args": { "currentObject": { "widget": "p.MyFirstModule.Restaurant_Overview.listView1", "source": "object" } } }
                                            })}
                                            renderMode={"span"} />
                                    ]
                                })}
                                pageSize={10} />
                        ]} />
                ]} />
        ]} />
]}</PageFragment>);

export const title = t([
    "Restaurant Overview"
]);

export const classes = "layout-atlas layout-atlas-responsive-default";

export const style = {};
export const content = { ...parentContent,
    "Atlas_Core.Atlas_Default.Main": region$Main,
};
