from shopwareapi.core.basefield import BaseField
from shopwareapi.core.basemodel import BaseModel
from shopwareapi.controller.currency import CurrencyController
from shopwareapi.utils.converter import Convert


class Currency(BaseModel):
    CONTROLLER_CLASS = CurrencyController

    FIELDS = (
        BaseField("id", "id", aliases=["currencyId"], required=False),
        BaseField("factor", "factor", required=False),
        BaseField("symbol", "symbol", required=False),
        BaseField("isoCode", "isoCode", required=False),
        BaseField("shortName", "shortName", required=False),
        BaseField("name", "name", required=False),
        BaseField("decimalPrecision", "decimalPrecision", required=False),
        BaseField("position", "position", required=False, converter=Convert.to_int),
        BaseField("isSystemDefault", "isSystemDefault", required=False),
        BaseField("customFields", "customFields", required=False),
        BaseField("createdAt", "createdAt", required=False),
        BaseField("updatedAt", "updatedAt", required=False)
    )

    @staticmethod
    def convert(client, data, field, key):
        currency = data.get(key)

        if isinstance(currency, Currency):
            return "currency", currency
        elif key == "currencyId":
            model = client().controller.Currency.get(currency)
            return "currency", model

# {
# 	"data": [{
# 		"id": "582f86e0509e431593b2854a4613f1d7",
# 		"type": "currency",
# 		"attributes": {
# 			"factor": 1.1,
# 			"symbol": "Fr",
# 			"isoCode": "CHF",
# 			"shortName": "CHF",
# 			"name": "Swiss francs",
# 			"decimalPrecision": 2,
# 			"position": 1,
# 			"isSystemDefault": false,
# 			"customFields": null,
# 			"createdAt": "2020-09-01T10:40:57.263+00:00",
# 			"updatedAt": null,
# 			"translated": {
# 				"shortName": "CHF",
# 				"name": "Swiss francs",
# 				"customFields": []
# 			},
# 			"apiAlias": null
# 		},
# 		"links": {
# 			"self": "http:\/\/localhost:8000\/api\/v3\/currency\/582f86e0509e431593b2854a4613f1d7"
# 		},
# 		"relationships": {
# 			"translations": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/582f86e0509e431593b2854a4613f1d7\/translations"
# 				}
# 			},
# 			"salesChannelDefaultAssignments": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/582f86e0509e431593b2854a4613f1d7\/sales-channel-default-assignments"
# 				}
# 			},
# 			"orders": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/582f86e0509e431593b2854a4613f1d7\/orders"
# 				}
# 			},
# 			"salesChannels": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/582f86e0509e431593b2854a4613f1d7\/sales-channels"
# 				}
# 			},
# 			"salesChannelDomains": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/582f86e0509e431593b2854a4613f1d7\/sales-channel-domains"
# 				}
# 			},
# 			"promotionDiscountPrices": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/582f86e0509e431593b2854a4613f1d7\/promotion-discount-prices"
# 				}
# 			},
# 			"productExports": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/582f86e0509e431593b2854a4613f1d7\/product-exports"
# 				}
# 			}
# 		},
# 		"meta": null
# 	}, {
# 		"id": "44b2f49da54f4a0c8312f28588aec5d4",
# 		"type": "currency",
# 		"attributes": {
# 			"factor": 26.735,
# 			"symbol": "K\u010d",
# 			"isoCode": "CZK",
# 			"shortName": "CZK",
# 			"name": "Czech koruna",
# 			"decimalPrecision": 2,
# 			"position": 1,
# 			"isSystemDefault": false,
# 			"customFields": null,
# 			"createdAt": "2020-09-01T10:41:04.241+00:00",
# 			"updatedAt": null,
# 			"translated": {
# 				"shortName": "CZK",
# 				"name": "Czech koruna",
# 				"customFields": []
# 			},
# 			"apiAlias": null
# 		},
# 		"links": {
# 			"self": "http:\/\/localhost:8000\/api\/v3\/currency\/44b2f49da54f4a0c8312f28588aec5d4"
# 		},
# 		"relationships": {
# 			"translations": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/44b2f49da54f4a0c8312f28588aec5d4\/translations"
# 				}
# 			},
# 			"salesChannelDefaultAssignments": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/44b2f49da54f4a0c8312f28588aec5d4\/sales-channel-default-assignments"
# 				}
# 			},
# 			"orders": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/44b2f49da54f4a0c8312f28588aec5d4\/orders"
# 				}
# 			},
# 			"salesChannels": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/44b2f49da54f4a0c8312f28588aec5d4\/sales-channels"
# 				}
# 			},
# 			"salesChannelDomains": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/44b2f49da54f4a0c8312f28588aec5d4\/sales-channel-domains"
# 				}
# 			},
# 			"promotionDiscountPrices": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/44b2f49da54f4a0c8312f28588aec5d4\/promotion-discount-prices"
# 				}
# 			},
# 			"productExports": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/44b2f49da54f4a0c8312f28588aec5d4\/product-exports"
# 				}
# 			}
# 		},
# 		"meta": null
# 	}, {
# 		"id": "dac4f005fb164839a6253355dee54e5c",
# 		"type": "currency",
# 		"attributes": {
# 			"factor": 7.47,
# 			"symbol": "kr",
# 			"isoCode": "DKK",
# 			"shortName": "DKK",
# 			"name": "Danish krone",
# 			"decimalPrecision": 2,
# 			"position": 1,
# 			"isSystemDefault": false,
# 			"customFields": null,
# 			"createdAt": "2020-09-01T10:40:57.272+00:00",
# 			"updatedAt": null,
# 			"translated": {
# 				"shortName": "DKK",
# 				"name": "Danish krone",
# 				"customFields": []
# 			},
# 			"apiAlias": null
# 		},
# 		"links": {
# 			"self": "http:\/\/localhost:8000\/api\/v3\/currency\/dac4f005fb164839a6253355dee54e5c"
# 		},
# 		"relationships": {
# 			"translations": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/dac4f005fb164839a6253355dee54e5c\/translations"
# 				}
# 			},
# 			"salesChannelDefaultAssignments": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/dac4f005fb164839a6253355dee54e5c\/sales-channel-default-assignments"
# 				}
# 			},
# 			"orders": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/dac4f005fb164839a6253355dee54e5c\/orders"
# 				}
# 			},
# 			"salesChannels": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/dac4f005fb164839a6253355dee54e5c\/sales-channels"
# 				}
# 			},
# 			"salesChannelDomains": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/dac4f005fb164839a6253355dee54e5c\/sales-channel-domains"
# 				}
# 			},
# 			"promotionDiscountPrices": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/dac4f005fb164839a6253355dee54e5c\/promotion-discount-prices"
# 				}
# 			},
# 			"productExports": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/dac4f005fb164839a6253355dee54e5c\/product-exports"
# 				}
# 			}
# 		},
# 		"meta": null
# 	}, {
# 		"id": "b7d2554b0ce847cd82f3ac9bd1c0dfca",
# 		"type": "currency",
# 		"attributes": {
# 			"factor": 1.0,
# 			"symbol": "\u20ac",
# 			"isoCode": "EUR",
# 			"shortName": "EUR",
# 			"name": "Euro",
# 			"decimalPrecision": 2,
# 			"position": 1,
# 			"isSystemDefault": true,
# 			"customFields": null,
# 			"createdAt": "2020-09-01T10:40:50.314+00:00",
# 			"updatedAt": null,
# 			"translated": {
# 				"shortName": "EUR",
# 				"name": "Euro",
# 				"customFields": []
# 			},
# 			"apiAlias": null
# 		},
# 		"links": {
# 			"self": "http:\/\/localhost:8000\/api\/v3\/currency\/b7d2554b0ce847cd82f3ac9bd1c0dfca"
# 		},
# 		"relationships": {
# 			"translations": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/b7d2554b0ce847cd82f3ac9bd1c0dfca\/translations"
# 				}
# 			},
# 			"salesChannelDefaultAssignments": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/b7d2554b0ce847cd82f3ac9bd1c0dfca\/sales-channel-default-assignments"
# 				}
# 			},
# 			"orders": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/b7d2554b0ce847cd82f3ac9bd1c0dfca\/orders"
# 				}
# 			},
# 			"salesChannels": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/b7d2554b0ce847cd82f3ac9bd1c0dfca\/sales-channels"
# 				}
# 			},
# 			"salesChannelDomains": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/b7d2554b0ce847cd82f3ac9bd1c0dfca\/sales-channel-domains"
# 				}
# 			},
# 			"promotionDiscountPrices": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/b7d2554b0ce847cd82f3ac9bd1c0dfca\/promotion-discount-prices"
# 				}
# 			},
# 			"productExports": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/b7d2554b0ce847cd82f3ac9bd1c0dfca\/product-exports"
# 				}
# 			}
# 		},
# 		"meta": null
# 	}, {
# 		"id": "bfd3ca7f9f664ca993c095769e877370",
# 		"type": "currency",
# 		"attributes": {
# 			"factor": 0.89157,
# 			"symbol": "\u00a3",
# 			"isoCode": "GBP",
# 			"shortName": "GBP",
# 			"name": "Pound",
# 			"decimalPrecision": 2,
# 			"position": 1,
# 			"isSystemDefault": false,
# 			"customFields": null,
# 			"createdAt": "2020-09-01T10:40:50.324+00:00",
# 			"updatedAt": null,
# 			"translated": {
# 				"shortName": "GBP",
# 				"name": "Pound",
# 				"customFields": []
# 			},
# 			"apiAlias": null
# 		},
# 		"links": {
# 			"self": "http:\/\/localhost:8000\/api\/v3\/currency\/bfd3ca7f9f664ca993c095769e877370"
# 		},
# 		"relationships": {
# 			"translations": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/bfd3ca7f9f664ca993c095769e877370\/translations"
# 				}
# 			},
# 			"salesChannelDefaultAssignments": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/bfd3ca7f9f664ca993c095769e877370\/sales-channel-default-assignments"
# 				}
# 			},
# 			"orders": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/bfd3ca7f9f664ca993c095769e877370\/orders"
# 				}
# 			},
# 			"salesChannels": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/bfd3ca7f9f664ca993c095769e877370\/sales-channels"
# 				}
# 			},
# 			"salesChannelDomains": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/bfd3ca7f9f664ca993c095769e877370\/sales-channel-domains"
# 				}
# 			},
# 			"promotionDiscountPrices": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/bfd3ca7f9f664ca993c095769e877370\/promotion-discount-prices"
# 				}
# 			},
# 			"productExports": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/bfd3ca7f9f664ca993c095769e877370\/product-exports"
# 				}
# 			}
# 		},
# 		"meta": null
# 	}, {
# 		"id": "036e38d2710f4938b944c33a99c2a35d",
# 		"type": "currency",
# 		"attributes": {
# 			"factor": 0.099,
# 			"symbol": "nkr",
# 			"isoCode": "NOK",
# 			"shortName": "NOK",
# 			"name": "Norwegian krone",
# 			"decimalPrecision": 2,
# 			"position": 1,
# 			"isSystemDefault": false,
# 			"customFields": null,
# 			"createdAt": "2020-09-01T10:40:57.276+00:00",
# 			"updatedAt": null,
# 			"translated": {
# 				"shortName": "NOK",
# 				"name": "Norwegian krone",
# 				"customFields": []
# 			},
# 			"apiAlias": null
# 		},
# 		"links": {
# 			"self": "http:\/\/localhost:8000\/api\/v3\/currency\/036e38d2710f4938b944c33a99c2a35d"
# 		},
# 		"relationships": {
# 			"translations": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/036e38d2710f4938b944c33a99c2a35d\/translations"
# 				}
# 			},
# 			"salesChannelDefaultAssignments": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/036e38d2710f4938b944c33a99c2a35d\/sales-channel-default-assignments"
# 				}
# 			},
# 			"orders": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/036e38d2710f4938b944c33a99c2a35d\/orders"
# 				}
# 			},
# 			"salesChannels": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/036e38d2710f4938b944c33a99c2a35d\/sales-channels"
# 				}
# 			},
# 			"salesChannelDomains": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/036e38d2710f4938b944c33a99c2a35d\/sales-channel-domains"
# 				}
# 			},
# 			"promotionDiscountPrices": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/036e38d2710f4938b944c33a99c2a35d\/promotion-discount-prices"
# 				}
# 			},
# 			"productExports": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/036e38d2710f4938b944c33a99c2a35d\/product-exports"
# 				}
# 			}
# 		},
# 		"meta": null
# 	}, {
# 		"id": "eeeef489bd83429e8b253eb6a7576076",
# 		"type": "currency",
# 		"attributes": {
# 			"factor": 4.33,
# 			"symbol": "z\u0142",
# 			"isoCode": "PLN",
# 			"shortName": "PLN",
# 			"name": "Z\u0142oty",
# 			"decimalPrecision": 2,
# 			"position": 1,
# 			"isSystemDefault": false,
# 			"customFields": null,
# 			"createdAt": "2020-09-01T10:40:57.255+00:00",
# 			"updatedAt": null,
# 			"translated": {
# 				"shortName": "PLN",
# 				"name": "Z\u0142oty",
# 				"customFields": []
# 			},
# 			"apiAlias": null
# 		},
# 		"links": {
# 			"self": "http:\/\/localhost:8000\/api\/v3\/currency\/eeeef489bd83429e8b253eb6a7576076"
# 		},
# 		"relationships": {
# 			"translations": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/eeeef489bd83429e8b253eb6a7576076\/translations"
# 				}
# 			},
# 			"salesChannelDefaultAssignments": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/eeeef489bd83429e8b253eb6a7576076\/sales-channel-default-assignments"
# 				}
# 			},
# 			"orders": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/eeeef489bd83429e8b253eb6a7576076\/orders"
# 				}
# 			},
# 			"salesChannels": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/eeeef489bd83429e8b253eb6a7576076\/sales-channels"
# 				}
# 			},
# 			"salesChannelDomains": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/eeeef489bd83429e8b253eb6a7576076\/sales-channel-domains"
# 				}
# 			},
# 			"promotionDiscountPrices": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/eeeef489bd83429e8b253eb6a7576076\/promotion-discount-prices"
# 				}
# 			},
# 			"productExports": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/eeeef489bd83429e8b253eb6a7576076\/product-exports"
# 				}
# 			}
# 		},
# 		"meta": null
# 	}, {
# 		"id": "713bc47374dd45ab9b849590e173f30d",
# 		"type": "currency",
# 		"attributes": {
# 			"factor": 10.51,
# 			"symbol": "kr",
# 			"isoCode": "SEK",
# 			"shortName": "SEK",
# 			"name": "Swedish krone",
# 			"decimalPrecision": 2,
# 			"position": 1,
# 			"isSystemDefault": false,
# 			"customFields": null,
# 			"createdAt": "2020-09-01T10:40:57.268+00:00",
# 			"updatedAt": null,
# 			"translated": {
# 				"shortName": "SEK",
# 				"name": "Swedish krone",
# 				"customFields": []
# 			},
# 			"apiAlias": null
# 		},
# 		"links": {
# 			"self": "http:\/\/localhost:8000\/api\/v3\/currency\/713bc47374dd45ab9b849590e173f30d"
# 		},
# 		"relationships": {
# 			"translations": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/713bc47374dd45ab9b849590e173f30d\/translations"
# 				}
# 			},
# 			"salesChannelDefaultAssignments": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/713bc47374dd45ab9b849590e173f30d\/sales-channel-default-assignments"
# 				}
# 			},
# 			"orders": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/713bc47374dd45ab9b849590e173f30d\/orders"
# 				}
# 			},
# 			"salesChannels": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/713bc47374dd45ab9b849590e173f30d\/sales-channels"
# 				}
# 			},
# 			"salesChannelDomains": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/713bc47374dd45ab9b849590e173f30d\/sales-channel-domains"
# 				}
# 			},
# 			"promotionDiscountPrices": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/713bc47374dd45ab9b849590e173f30d\/promotion-discount-prices"
# 				}
# 			},
# 			"productExports": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/713bc47374dd45ab9b849590e173f30d\/product-exports"
# 				}
# 			}
# 		},
# 		"meta": null
# 	}, {
# 		"id": "601827f029ee4852a88a3bb61439d181",
# 		"type": "currency",
# 		"attributes": {
# 			"factor": 1.17085,
# 			"symbol": "$",
# 			"isoCode": "USD",
# 			"shortName": "USD",
# 			"name": "US-Dollar",
# 			"decimalPrecision": 2,
# 			"position": 1,
# 			"isSystemDefault": false,
# 			"customFields": null,
# 			"createdAt": "2020-09-01T10:40:50.320+00:00",
# 			"updatedAt": null,
# 			"translated": {
# 				"shortName": "USD",
# 				"name": "US-Dollar",
# 				"customFields": []
# 			},
# 			"apiAlias": null
# 		},
# 		"links": {
# 			"self": "http:\/\/localhost:8000\/api\/v3\/currency\/601827f029ee4852a88a3bb61439d181"
# 		},
# 		"relationships": {
# 			"translations": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/601827f029ee4852a88a3bb61439d181\/translations"
# 				}
# 			},
# 			"salesChannelDefaultAssignments": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/601827f029ee4852a88a3bb61439d181\/sales-channel-default-assignments"
# 				}
# 			},
# 			"orders": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/601827f029ee4852a88a3bb61439d181\/orders"
# 				}
# 			},
# 			"salesChannels": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/601827f029ee4852a88a3bb61439d181\/sales-channels"
# 				}
# 			},
# 			"salesChannelDomains": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/601827f029ee4852a88a3bb61439d181\/sales-channel-domains"
# 				}
# 			},
# 			"promotionDiscountPrices": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/601827f029ee4852a88a3bb61439d181\/promotion-discount-prices"
# 				}
# 			},
# 			"productExports": {
# 				"data": [],
# 				"links": {
# 					"related": "http:\/\/localhost:8000\/api\/v3\/currency\/601827f029ee4852a88a3bb61439d181\/product-exports"
# 				}
# 			}
# 		},
# 		"meta": null
# 	}],
# 	"included": [],
# 	"links": {
# 		"first": "http:\/\/localhost:8000\/api\/v3\/search\/currency?limit=500&page=1",
# 		"last": "http:\/\/localhost:8000\/api\/v3\/search\/currency?limit=500&page=1",
# 		"self": "http:\/\/localhost:8000\/api\/v3\/search\/currency"
# 	},
# 	"meta": {
# 		"totalCountMode": 1,
# 		"total": 9
# 	},
# 	"aggregations": []
# }
