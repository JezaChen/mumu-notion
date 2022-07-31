""" Example data """


class PageExampleData:
    # Be careful:
    # The parent of the example page is A PAGE!
    # ---
    CREATE_EXAMPLE: dict = {
        "cover": {
            "type": "external",
            "external": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/6/62/Tuscankale.jpg"
            }
        },
        "icon": {
            "type": "emoji",
            "emoji": "🥬"
        },
        "parent": {
            "type": "page_id",  # The default parent is page
            "page_id": ""  # Need to fill
        },
        "properties": {
            "title": [
                {
                    "text": {
                        "content": "Tuscan kale"
                    }
                }
            ]
        },
        "children": [
            {
                "object": "block",
                "heading_2": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Lacinato kale"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "paragraph": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Lacinato kale is a variety of kale with a long tradition in Italian cuisine, especially that of Tuscany. It is also known as Tuscan kale, Italian kale, dinosaur kale, kale, flat back kale, palm tree kale, or black Tuscan palm.",
                                "link": {
                                    "url": "https://en.wikipedia.org/wiki/Lacinato_kale"
                                }
                            },
                            "href": "https://en.wikipedia.org/wiki/Lacinato_kale"
                        }
                    ],
                    "color": "default"
                }
            }
        ]
    }

    UPDATE_EXAMPLE = {
        "properties": {
            "title": [
                {
                    "text": {
                        "content": "A new title created by PyNotion!"
                    }
                }
            ]
        }
    }


class BlockExampleData:
    HEADING2_BLOCK_UPDATE_DATA_EXAMPLE = {
        "heading_2": {
            "rich_text": [
                {
                    "text": {
                        "content": "Lacinato kale (Updated by mumu-notion!)"
                    },
                    "annotations": {
                        "color": "green"
                    }
                }
            ]
        }
    }

    CHILD_BLOCK_APPEND_DATA_EXAMPLE = {
        "children": [
            {
                "heading_2": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Lacinato kale"
                            }
                        }
                    ]
                }
            },
            {
                "paragraph": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Lacinato kale is a variety of kale with a long tradition in Italian cuisine, especially that of Tuscany. It is also known as Tuscan kale, Italian kale, dinosaur kale, kale, flat back kale, palm tree kale, or black Tuscan palm.",
                                "link": {
                                    "url": "https://en.wikipedia.org/wiki/Lacinato_kale"
                                }
                            }
                        }
                    ]
                }
            }
        ]
    }


class DatabaseExampleData:
    MEAL_CREATE_EXAMPLE = {
        "parent": {
            "type": "page_id",
            "page_id": ""
        },
        "title": [
            {
                "type": "text",
                "text": {
                    "content": "Meal List",
                    "link": None
                }
            }
        ],
        "properties": {
            "Name": {
                "title": {}
            },
        }
    }

    GROCERY_CREATE_EXAMPLE = {
        "parent": {
            "type": "page_id",
            "page_id": ""  # need to fill
        },
        "title": [
            {
                "type": "text",
                "text": {
                    "content": "Grocery List",
                    "link": None
                }
            }
        ],
        "properties": {
            "Name": {
                "title": {}
            },
            "Description": {
                "rich_text": {}
            },
            "In stock": {
                "checkbox": {}
            },
            "Food group": {
                "select": {
                    "options": [
                        {
                            "name": "🥦Vegetable",
                            "color": "green"
                        },
                        {
                            "name": "🍎Fruit",
                            "color": "red"
                        },
                        {
                            "name": "💪Protein",
                            "color": "yellow"
                        }
                    ]
                }
            },
            "Price": {
                "number": {
                    "format": "dollar"
                }
            },
            "Last ordered": {
                "date": {}
            },
            "Meals": {
                "relation": {
                    "database_id": "",  # need to fill
                    "single_property": {}
                }
            },
            "Number of meals": {
                "rollup": {
                    "rollup_property_name": "Name",
                    "relation_property_name": "Meals",
                    "function": "count"
                }
            },
            "Store availability": {
                "type": "multi_select",
                "multi_select": {
                    "options": [
                        {
                            "name": "Duc Loi Market",
                            "color": "blue"
                        },
                        {
                            "name": "Rainbow Grocery",
                            "color": "gray"
                        },
                        {
                            "name": "Nijiya Market",
                            "color": "purple"
                        },
                        {
                            "name": "Gus'\''s Community Market",
                            "color": "yellow"
                        }
                    ]
                }
            },
            "+1": {
                "people": {}
            },
            "Photo": {
                "files": {}
            }
        }
    }

    GROCERY_UPDATE_EXAMPLE = {
        "title": [
            {
                "text": {
                    "content": "Today'\''s official_guides list"
                }
            }
        ],
        "description": [
            {
                "text": {
                    "content": "Grocery list for just kale 🥬 (updated by mumu-notion!)"
                }
            }
        ],
        "properties": {
            "+1": None,
            "Photo": {
                "url": {}
            },
            "Store availability": {
                "multi_select": {
                    "options": [
                        {
                            "name": "Duc Loi Market"
                        },
                        {
                            "name": "Rainbow Grocery"
                        },
                        {
                            "name": "Gus'\''s Community Market"
                        },
                        {
                            "name": "The Good Life Grocery",
                        },
                        {
                            "name": "Walmart",
                            "color": "gray"
                        }
                    ]
                }
            }
        }
    }


class CommentExampleData:
    COMMENT_DATA_EXAMPLE = {
        "parent": {
            "page_id": ""  # need to fill
        },
        "rich_text": [
            {
                "text": {
                    "content": "Hello world"
                }
            }
        ]
    }
