import { createElement } from "react";
const React = { createElement };

import { PageFragment } from "mendix/PageFragment";
import { DatabaseObjectListProperty } from "mendix/DatabaseObjectListProperty";
import { ExpressionProperty } from "mendix/ExpressionProperty";
import { TemplatedWidgetProperty } from "mendix/TemplatedWidgetProperty";
import { TextProperty } from "mendix/TextProperty";

import { Container } from "mendix/widgets/web/Container";
import { Div } from "mendix/widgets/web/Div";
import * as ImageWidgetModule from "C:/Users/Korisnik/Mendix/FoodDelivery2-main/deployment/web/widgets/com/mendix/widget/web/image/Image.mjs";
const Image = Object.getOwnPropertyDescriptor(ImageWidgetModule, "Image")?.value || Object.getOwnPropertyDescriptor(ImageWidgetModule, "default")?.value;   
import "C:/Users/Korisnik/Mendix/FoodDelivery2-main/deployment/web/widgets/com/mendix/widget/web/image/Image.css";
import { ListView } from "mendix/widgets/web/ListView";
import { TabContainer } from "mendix/widgets/web/TabContainer";
import { Text } from "mendix/widgets/web/Text";
import { addEnumerations, asPluginWidgets, t } from "mendix";

import { content as parentContent } from "../layouts/Atlas_Core.Atlas_Default.js";

const { $Div, $TabContainer, $ListView, $Image, $Container, $Text } = asPluginWidgets({ Div, TabContainer, ListView, Image, Container, Text });

const region$Main = (historyId) => (<PageFragment renderKey={historyId}>{[
    <$Div key="p.MyFirstModule.RestaurantCatalog.layoutGrid1"
        $widgetId="p.MyFirstModule.RestaurantCatalog.layoutGrid1"
        class={"mx-name-layoutGrid1 mx-layoutgrid mx-layoutgrid-fluid container-fluid"}
        content={[
            <$Div key="p.MyFirstModule.RestaurantCatalog.layoutGrid1$row0"
                $widgetId="p.MyFirstModule.RestaurantCatalog.layoutGrid1$row0"
                class={"row"}
                content={[
                    <$Div key="p.MyFirstModule.RestaurantCatalog.layoutGrid1$row0$column0"
                        $widgetId="p.MyFirstModule.RestaurantCatalog.layoutGrid1$row0$column0"
                        class={"col-lg-12 col-md-12 col-12"}
                        content={[
                            <$TabContainer key="p.MyFirstModule.RestaurantCatalog.tabContainer1"
                                $widgetId="p.MyFirstModule.RestaurantCatalog.tabContainer1"
                                class={"mx-name-tabContainer1"}
                                widgetId={"p.MyFirstModule.RestaurantCatalog.tabContainer1"}
                                defaultTab={0}
                                tabs={[
                                    {
                                        "name": "tabPage1",
                                        "caption": TextProperty({
                                            "value": "Sv atkl"
                                        }),
                                        "isDelayed": false,
                                        "refreshOnShow": false,
                                        "content": [
                                            <$ListView key="p.MyFirstModule.RestaurantCatalog.listView1"
                                                $widgetId="p.MyFirstModule.RestaurantCatalog.listView1"
                                                class={"mx-name-listView1"}
                                                listValue={DatabaseObjectListProperty({
                                                    "dataSourceId": "p.2",
                                                    "entity": "MyFirstModule.ItemAPI",
                                                    "scope": "$RestaurantAPI",
                                                    "operationId": "+kCsHNQ8e1KVzhOTvF4OEw",
                                                    "sort": []
                                                })}
                                                itemTemplate={TemplatedWidgetProperty({
                                                    "dataSourceId": "p.2",
                                                    "editable": false,
                                                    "children": () => [
                                                        <$Image key="p.MyFirstModule.RestaurantCatalog.image1"
                                                            $widgetId="p.MyFirstModule.RestaurantCatalog.image1"
                                                            datasource={"imageUrl"}
                                                            imageUrl={ExpressionProperty({
                                                                "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "imageUrl" }, "args": { "currentObject": { "widget": "p.MyFirstModule.RestaurantCatalog.listView1", "source": "object" } } }
                                                            })}
                                                            isBackgroundImage={false}
                                                            onClickType={"action"}
                                                            alternativeText={ExpressionProperty({
                                                                "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                            })}
                                                            widthUnit={"auto"}
                                                            width={100}
                                                            heightUnit={"auto"}
                                                            height={100}
                                                            iconSize={14}
                                                            displayAs={"fullImage"}
                                                            responsive={true}
                                                            class={"mx-name-image1"} />,
                                                        <$Container key="p.MyFirstModule.RestaurantCatalog.container1"
                                                            $widgetId="p.MyFirstModule.RestaurantCatalog.container1"
                                                            class={"mx-name-container1 card"}
                                                            renderMode={"div"}
                                                            content={[
                                                                <$Text key="p.MyFirstModule.RestaurantCatalog.text2"
                                                                    $widgetId="p.MyFirstModule.RestaurantCatalog.text2"
                                                                    class={"mx-name-text2"}
                                                                    caption={ExpressionProperty({
                                                                        "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "Name" }, "args": { "currentObject": { "widget": "p.MyFirstModule.RestaurantCatalog.listView1", "source": "object" } } }
                                                                    })}
                                                                    renderMode={"h2"} />,
                                                                <$Text key="p.MyFirstModule.RestaurantCatalog.text3"
                                                                    $widgetId="p.MyFirstModule.RestaurantCatalog.text3"
                                                                    class={"mx-name-text3"}
                                                                    caption={ExpressionProperty({
                                                                        "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "description" }, "args": { "currentObject": { "widget": "p.MyFirstModule.RestaurantCatalog.listView1", "source": "object" } } }
                                                                    })}
                                                                    renderMode={"h4"} />,
                                                                <$Text key="p.MyFirstModule.RestaurantCatalog.text9"
                                                                    $widgetId="p.MyFirstModule.RestaurantCatalog.text9"
                                                                    class={"mx-name-text9"}
                                                                    caption={ExpressionProperty({
                                                                        "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "MyFirstModule.ItemAPI_Order/MyFirstModule.Order/DriverAvailability" }, "args": { "currentObject": { "widget": "p.MyFirstModule.RestaurantCatalog.listView1", "source": "object" } } }
                                                                    })}
                                                                    renderMode={"h5"} />,
                                                                <$Text key="p.MyFirstModule.RestaurantCatalog.text6"
                                                                    $widgetId="p.MyFirstModule.RestaurantCatalog.text6"
                                                                    class={"mx-name-text6"}
                                                                    caption={ExpressionProperty({
                                                                        "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "imageUrl" }, "args": { "currentObject": { "widget": "p.MyFirstModule.RestaurantCatalog.listView1", "source": "object" } } }
                                                                    })}
                                                                    renderMode={"span"} />,
                                                                <$Text key="p.MyFirstModule.RestaurantCatalog.text7"
                                                                    $widgetId="p.MyFirstModule.RestaurantCatalog.text7"
                                                                    class={"mx-name-text7"}
                                                                    caption={ExpressionProperty({
                                                                        "expression": { "expr": { "type": "function", "name": "_format", "parameters": [ { "type": "variable", "variable": "currentObject", "path": "price" }, { "type": "literal", "value": "{\"decimalPrecision\":2}" } ] }, "args": { "currentObject": { "widget": "p.MyFirstModule.RestaurantCatalog.listView1", "source": "object" } } }
                                                                    })}
                                                                    renderMode={"span"} />,
                                                                <$Text key="p.MyFirstModule.RestaurantCatalog.text5"
                                                                    $widgetId="p.MyFirstModule.RestaurantCatalog.text5"
                                                                    class={"mx-name-text5"}
                                                                    caption={ExpressionProperty({
                                                                        "expression": { "expr": { "type": "function", "name": "_format", "parameters": [ { "type": "variable", "variable": "currentObject", "path": "available" }, { "type": "literal", "value": "{}" } ] }, "args": { "currentObject": { "widget": "p.MyFirstModule.RestaurantCatalog.listView1", "source": "object" } } }
                                                                    })}
                                                                    renderMode={"span"} />,
                                                                <$Text key="p.MyFirstModule.RestaurantCatalog.text4"
                                                                    $widgetId="p.MyFirstModule.RestaurantCatalog.text4"
                                                                    class={"mx-name-text4"}
                                                                    caption={ExpressionProperty({
                                                                        "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "category" }, "args": { "currentObject": { "widget": "p.MyFirstModule.RestaurantCatalog.listView1", "source": "object" } } }
                                                                    })}
                                                                    renderMode={"span"} />
                                                            ]}
                                                            ariaHidden={false} />
                                                    ]
                                                })}
                                                pageSize={10} />
                                        ]
                                    },
                                    {
                                        "name": "tabPage2",
                                        "caption": TextProperty({
                                            "value": "Page 2"
                                        }),
                                        "isDelayed": true,
                                        "refreshOnShow": false,
                                        "content": [
                                            <$ListView key="p.MyFirstModule.RestaurantCatalog.listView2"
                                                $widgetId="p.MyFirstModule.RestaurantCatalog.listView2"
                                                class={"mx-name-listView2"}
                                                listValue={DatabaseObjectListProperty({
                                                    "dataSourceId": "p.3",
                                                    "entity": "MyFirstModule.ItemAPI",
                                                    "scope": "$RestaurantAPI",
                                                    "operationId": "qVQ5EfWOgV6lIn2SrKHOEw",
                                                    "sort": []
                                                })}
                                                itemTemplate={TemplatedWidgetProperty({
                                                    "dataSourceId": "p.3",
                                                    "editable": false,
                                                    "children": () => [
                                                        <$Image key="p.MyFirstModule.RestaurantCatalog.image2"
                                                            $widgetId="p.MyFirstModule.RestaurantCatalog.image2"
                                                            datasource={"imageUrl"}
                                                            imageUrl={ExpressionProperty({
                                                                "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "imageUrl" }, "args": { "currentObject": { "widget": "p.MyFirstModule.RestaurantCatalog.listView2", "source": "object" } } }
                                                            })}
                                                            isBackgroundImage={false}
                                                            onClickType={"action"}
                                                            alternativeText={ExpressionProperty({
                                                                "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                            })}
                                                            widthUnit={"auto"}
                                                            width={100}
                                                            heightUnit={"auto"}
                                                            height={100}
                                                            iconSize={14}
                                                            displayAs={"fullImage"}
                                                            responsive={true}
                                                            class={"mx-name-image2"} />,
                                                        <$Container key="p.MyFirstModule.RestaurantCatalog.container2"
                                                            $widgetId="p.MyFirstModule.RestaurantCatalog.container2"
                                                            class={"mx-name-container2 card"}
                                                            renderMode={"div"}
                                                            content={[
                                                                <$Text key="p.MyFirstModule.RestaurantCatalog.text8"
                                                                    $widgetId="p.MyFirstModule.RestaurantCatalog.text8"
                                                                    class={"mx-name-text8"}
                                                                    caption={ExpressionProperty({
                                                                        "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "Name" }, "args": { "currentObject": { "widget": "p.MyFirstModule.RestaurantCatalog.listView2", "source": "object" } } }
                                                                    })}
                                                                    renderMode={"h2"} />,
                                                                <$Text key="p.MyFirstModule.RestaurantCatalog.text10"
                                                                    $widgetId="p.MyFirstModule.RestaurantCatalog.text10"
                                                                    class={"mx-name-text10"}
                                                                    caption={ExpressionProperty({
                                                                        "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "description" }, "args": { "currentObject": { "widget": "p.MyFirstModule.RestaurantCatalog.listView2", "source": "object" } } }
                                                                    })}
                                                                    renderMode={"h4"} />,
                                                                <$Text key="p.MyFirstModule.RestaurantCatalog.text11"
                                                                    $widgetId="p.MyFirstModule.RestaurantCatalog.text11"
                                                                    class={"mx-name-text11"}
                                                                    caption={ExpressionProperty({
                                                                        "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "MyFirstModule.ItemAPI_Order/MyFirstModule.Order/DriverAvailability" }, "args": { "currentObject": { "widget": "p.MyFirstModule.RestaurantCatalog.listView2", "source": "object" } } }
                                                                    })}
                                                                    renderMode={"h5"} />,
                                                                <$Text key="p.MyFirstModule.RestaurantCatalog.text12"
                                                                    $widgetId="p.MyFirstModule.RestaurantCatalog.text12"
                                                                    class={"mx-name-text12"}
                                                                    caption={ExpressionProperty({
                                                                        "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "imageUrl" }, "args": { "currentObject": { "widget": "p.MyFirstModule.RestaurantCatalog.listView2", "source": "object" } } }
                                                                    })}
                                                                    renderMode={"span"} />,
                                                                <$Text key="p.MyFirstModule.RestaurantCatalog.text13"
                                                                    $widgetId="p.MyFirstModule.RestaurantCatalog.text13"
                                                                    class={"mx-name-text13"}
                                                                    caption={ExpressionProperty({
                                                                        "expression": { "expr": { "type": "function", "name": "_format", "parameters": [ { "type": "variable", "variable": "currentObject", "path": "price" }, { "type": "literal", "value": "{\"decimalPrecision\":2}" } ] }, "args": { "currentObject": { "widget": "p.MyFirstModule.RestaurantCatalog.listView2", "source": "object" } } }
                                                                    })}
                                                                    renderMode={"span"} />,
                                                                <$Text key="p.MyFirstModule.RestaurantCatalog.text14"
                                                                    $widgetId="p.MyFirstModule.RestaurantCatalog.text14"
                                                                    class={"mx-name-text14"}
                                                                    caption={ExpressionProperty({
                                                                        "expression": { "expr": { "type": "function", "name": "_format", "parameters": [ { "type": "variable", "variable": "currentObject", "path": "available" }, { "type": "literal", "value": "{}" } ] }, "args": { "currentObject": { "widget": "p.MyFirstModule.RestaurantCatalog.listView2", "source": "object" } } }
                                                                    })}
                                                                    renderMode={"span"} />,
                                                                <$Text key="p.MyFirstModule.RestaurantCatalog.text15"
                                                                    $widgetId="p.MyFirstModule.RestaurantCatalog.text15"
                                                                    class={"mx-name-text15"}
                                                                    caption={ExpressionProperty({
                                                                        "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "category" }, "args": { "currentObject": { "widget": "p.MyFirstModule.RestaurantCatalog.listView2", "source": "object" } } }
                                                                    })}
                                                                    renderMode={"span"} />
                                                            ]}
                                                            ariaHidden={false} />
                                                    ]
                                                })}
                                                pageSize={10} />
                                        ]
                                    }
                                ]} />
                        ]} />
                ]} />
        ]} />
]}</PageFragment>);

export const title = t([
    "Restaurant catalog"
]);

export const classes = "layout-atlas layout-atlas-responsive-default";

export const style = {};
export const content = { ...parentContent,
    "Atlas_Core.Atlas_Default.Main": region$Main,
};
