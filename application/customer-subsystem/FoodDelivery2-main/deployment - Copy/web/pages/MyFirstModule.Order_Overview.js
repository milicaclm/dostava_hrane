import { createElement } from "react";
const React = { createElement };

import { PageFragment } from "mendix/PageFragment";
import { DatabaseObjectListProperty } from "mendix/DatabaseObjectListProperty";
import { ExpressionProperty } from "mendix/ExpressionProperty";
import { TemplatedWidgetProperty } from "mendix/TemplatedWidgetProperty";

import { Div } from "mendix/widgets/web/Div";
import { ListView } from "mendix/widgets/web/ListView";
import { Text } from "mendix/widgets/web/Text";
import { addEnumerations, asPluginWidgets, t } from "mendix";

import { content as parentContent } from "../layouts/Atlas_Core.Atlas_Default.js";

const { $Div, $Text, $ListView } = asPluginWidgets({ Div, Text, ListView });

const region$Main = (historyId) => (<PageFragment renderKey={historyId}>{[
    <$Div key="p.MyFirstModule.Order_Overview.layoutGrid1"
        $widgetId="p.MyFirstModule.Order_Overview.layoutGrid1"
        class={"mx-name-layoutGrid1 mx-layoutgrid mx-layoutgrid-fluid container-fluid"}
        content={[
            <$Div key="p.MyFirstModule.Order_Overview.layoutGrid1$row0"
                $widgetId="p.MyFirstModule.Order_Overview.layoutGrid1$row0"
                class={"row"}
                content={[
                    <$Div key="p.MyFirstModule.Order_Overview.layoutGrid1$row0$column0"
                        $widgetId="p.MyFirstModule.Order_Overview.layoutGrid1$row0$column0"
                        class={"col-lg col-md col"}
                        content={[
                            <$Text key="p.MyFirstModule.Order_Overview.text1"
                                $widgetId="p.MyFirstModule.Order_Overview.text1"
                                class={"mx-name-text1"}
                                caption={ExpressionProperty({
                                    "expression": { "expr": { "type": "literal", "value": "My Orders" }, "args": {} }
                                })}
                                renderMode={"h2"} />,
                            <$ListView key="p.MyFirstModule.Order_Overview.listView1"
                                $widgetId="p.MyFirstModule.Order_Overview.listView1"
                                class={"mx-name-listView1"}
                                listValue={DatabaseObjectListProperty({
                                    "dataSourceId": "p.0",
                                    "entity": "MyFirstModule.Order",
                                    "operationId": "c+5EZ9W0hlK3iIvX/ER7ZA",
                                    "sort": [],
                                    "constraints": { "type": "function", "name": "!=", "parameters": [ { "type": "attribute", "attribute": "Status", "context": "MyFirstModule.Order", "attributeType": "#MyFirstModule.OrderStatus" }, { "type": "literal", "value": "Cart" } ] }
                                })}
                                itemTemplate={TemplatedWidgetProperty({
                                    "dataSourceId": "p.0",
                                    "editable": false,
                                    "children": () => [
                                        <$Div key="p.MyFirstModule.Order_Overview.layoutGrid2"
                                            $widgetId="p.MyFirstModule.Order_Overview.layoutGrid2"
                                            class={"mx-name-layoutGrid2 mx-layoutgrid mx-layoutgrid-fluid"}
                                            content={[
                                                <$Div key="p.MyFirstModule.Order_Overview.layoutGrid2$row0"
                                                    $widgetId="p.MyFirstModule.Order_Overview.layoutGrid2$row0"
                                                    class={"row"}
                                                    content={[
                                                        <$Div key="p.MyFirstModule.Order_Overview.layoutGrid2$row0$column0"
                                                            $widgetId="p.MyFirstModule.Order_Overview.layoutGrid2$row0$column0"
                                                            class={"col-lg col-md col"}
                                                            content={[
                                                                <$Text key="p.MyFirstModule.Order_Overview.RestaurantName"
                                                                    $widgetId="p.MyFirstModule.Order_Overview.RestaurantName"
                                                                    class={"mx-name-RestaurantName"}
                                                                    caption={ExpressionProperty({
                                                                        "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "MyFirstModule.Order_RestaurantAPI/MyFirstModule.RestaurantAPI/name" }, "args": { "currentObject": { "widget": "p.MyFirstModule.Order_Overview.listView1", "source": "object" } } }
                                                                    })}
                                                                    renderMode={"h4"} />
                                                            ]} />
                                                    ]} />,
                                                <$Div key="p.MyFirstModule.Order_Overview.layoutGrid2$row1"
                                                    $widgetId="p.MyFirstModule.Order_Overview.layoutGrid2$row1"
                                                    class={"row"}
                                                    content={[
                                                        <$Div key="p.MyFirstModule.Order_Overview.layoutGrid2$row1$column0"
                                                            $widgetId="p.MyFirstModule.Order_Overview.layoutGrid2$row1$column0"
                                                            class={"col-lg col-md col"}
                                                            content={[
                                                                <$Text key="p.MyFirstModule.Order_Overview.OrderStatus"
                                                                    $widgetId="p.MyFirstModule.Order_Overview.OrderStatus"
                                                                    class={"mx-name-OrderStatus"}
                                                                    caption={ExpressionProperty({
                                                                        "expression": { "expr": { "type": "function", "name": "+", "parameters": [ { "type": "literal", "value": "Status: " }, { "type": "function", "name": "getCaption", "parameters": [ { "type": "variable", "variable": "currentObject", "path": "Status" }, { "type": "literal", "value": "MyFirstModule.OrderStatus" } ] } ] }, "args": { "currentObject": { "widget": "p.MyFirstModule.Order_Overview.listView1", "source": "object" } } }
                                                                    })}
                                                                    renderMode={"span"} />
                                                            ]} />
                                                    ]} />,
                                                <$Div key="p.MyFirstModule.Order_Overview.layoutGrid2$row2"
                                                    $widgetId="p.MyFirstModule.Order_Overview.layoutGrid2$row2"
                                                    class={"row"}
                                                    content={[
                                                        <$Div key="p.MyFirstModule.Order_Overview.layoutGrid2$row2$column0"
                                                            $widgetId="p.MyFirstModule.Order_Overview.layoutGrid2$row2$column0"
                                                            class={"col-lg col-md col"}
                                                            content={[
                                                                <$Text key="p.MyFirstModule.Order_Overview.Total"
                                                                    $widgetId="p.MyFirstModule.Order_Overview.Total"
                                                                    class={"mx-name-Total"}
                                                                    caption={ExpressionProperty({
                                                                        "expression": { "expr": { "type": "function", "name": "+", "parameters": [ { "type": "function", "name": "+", "parameters": [ { "type": "literal", "value": "Total Price: " }, { "type": "function", "name": "_format", "parameters": [ { "type": "variable", "variable": "currentObject", "path": "TotalPrice" }, { "type": "literal", "value": "{\"decimalPrecision\":2}" } ] } ] }, { "type": "literal", "value": " RSD" } ] }, "args": { "currentObject": { "widget": "p.MyFirstModule.Order_Overview.listView1", "source": "object" } } }
                                                                    })}
                                                                    renderMode={"span"} />
                                                            ]} />
                                                    ]} />,
                                                <$Div key="p.MyFirstModule.Order_Overview.layoutGrid2$row3"
                                                    $widgetId="p.MyFirstModule.Order_Overview.layoutGrid2$row3"
                                                    class={"row"}
                                                    content={[
                                                        <$Div key="p.MyFirstModule.Order_Overview.layoutGrid2$row3$column0"
                                                            $widgetId="p.MyFirstModule.Order_Overview.layoutGrid2$row3$column0"
                                                            class={"col-lg col-md col"}
                                                            content={[
                                                                <$Text key="p.MyFirstModule.Order_Overview.Date"
                                                                    $widgetId="p.MyFirstModule.Order_Overview.Date"
                                                                    class={"mx-name-Date"}
                                                                    caption={ExpressionProperty({
                                                                        "expression": { "expr": { "type": "function", "name": "_format", "parameters": [ { "type": "variable", "variable": "currentObject", "path": "OrderDate" }, { "type": "literal", "value": "{\"type\":\"date\"}" } ] }, "args": { "currentObject": { "widget": "p.MyFirstModule.Order_Overview.listView1", "source": "object" } } }
                                                                    })}
                                                                    renderMode={"span"} />
                                                            ]} />
                                                    ]} />
                                            ]} />
                                    ]
                                })}
                                pageSize={10} />
                        ]} />
                ]} />
        ]} />
]}</PageFragment>);

export const title = t([
    "Order Overview"
]);

export const classes = "layout-atlas layout-atlas-responsive-default";

export const style = {};
export const content = { ...parentContent,
    "Atlas_Core.Atlas_Default.Main": region$Main,
};
