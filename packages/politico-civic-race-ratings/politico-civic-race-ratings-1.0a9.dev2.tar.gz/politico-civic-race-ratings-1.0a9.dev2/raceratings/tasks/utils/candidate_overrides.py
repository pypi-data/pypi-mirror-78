CANDIDATE_OVERRIDES = {
    "27127": {  # MS-SEN-R
        "27220": {
            "firstName": "Cindy",
            "middleName": None,
            "lastName": "Hyde-Smith",
            "suffix": None,
            "incumbent": True,
        }
    },
    "49392": {  # WA-R
        "51550": {
            "firstName": "Donald",
            "middleName": None,
            "lastName": "Trump",
            "suffix": None,
            "incumbent": True,
        }
    },
    "25927": {  # MS-01-R
        "27733": {
            "firstName": "Trent",
            "middleName": None,
            "lastName": "Kelly",
            "suffix": None,
            "incumbent": True,
        }
    },
    "26695": {  # MS-01-D
        "28664": {
            "firstName": "Antonia",
            "middleName": None,
            "lastName": "Eliason",
            "suffix": None,
            "incumbent": False,
        }
    },
    "": {
        "28664": {
            "firstName": "",
            "middleName": None,
            "lastName": "",
            "suffix": None,
            "incumbent": False,
        }
    }
    # House:
    # No second runoff winner found in race #"48452"
    # No second runoff winner found in race #"48453"
    # No second top-two winner found in race #"5958"
    # No second top-two winner found in race #"6035"
    # No second top-two winner found in race #"6043"
    # No second top-two winner found in race #"6044"
    # No second top-two winner found in race #"6056"
    # No second top-two winner found in race #"6059"
    # Senate:
    # No second runoff winner found in race #"48145"
}


PRIMARY_DATE_OVERRIDES = {
    "downticket": {"ID": "2020-06-02", "VA": "2020-06-23"},
    "president": {"CT": "2020-08-11", "DE": "2020-07-07"},
}

# Still TODO:
#   - WI-04 (R)  # Certified by Aug. 26
#   - FL-19 (R)  # Certification date unknown
#   - FL-20 (R)  # Certification date unknown
#   - FL-23 (R)  # Certification date unknown

WINNER_OVERRIDES = {
    # House:
    "38232": "41086",  # OR-02-D: Alex Spenser (outright + certified winner)
}

RUNOFF_DATES = {
    "AL": "2020-07-14",
    "MS": "2020-06-23",
    "NC": "2020-06-23",
    "TX": "2020-07-14",
    "GA": "2020-08-11",
    "OK": "2020-08-25",
}


SECOND_RUNOFF_OVERRIDES = {
    # House:
    # "48452": ["47078", "52498"],  # TX-17-R  # Pete Sessions  # Renee Swann
    # "48453": [  # TX-18-R
    #     "52506",  # Wendell Champion
    #     "52505",  # Robert Cadena
    # ],
    "5958": [  # CA-44-T2
        "12713",  # Nanette Barragan
        "13443",  # Analilia Joya
    ],
    "6035": ["7141", "13289"],  # CA-19-T2  # Zoe Lofgren  # Justin Aguilera
    "6043": ["8322", "13091"],  # CA-27-T2  # Judy Chu  # Johnny Nalbandian
    "6044": ["7009", "12973"],  # CA-28-T2  # Adam Schiff  # Eric Early
    "6056": [  # CA-40-T2
        "5359",  # Lucille Roybal-Allard
        "13438",  # C. Antonio Delgado
    ],
    "6059": ["5122", "13339"],  # CA-43-T2  # Maxine Waters  # Joe Collins
    # Senate:
    # "48145": ["51918", "46648"],  # TX-SEN-D  # MJ Hegar  # Royce West
}


UNTRACKED_CONTESTS = {
    "house": {
        "CA-13": {
            "placeOne": {
                "type": "topTwoPrimaryUnopposed",
                "firstName": "Barbara",
                "middleName": None,
                "lastName": "Lee",
                "suffix": None,
                "incumbent": True,
                "party": "dem",
            },
            "placeTwo": {
                "type": "topTwoPrimaryUnopposed",
                "firstName": "Nikka",
                "middleName": None,
                "lastName": "Piterman",
                "suffix": None,
                "incumbent": False,
                "party": "gop",
            },
        },
        "CA-51": {
            "placeOne": {
                "type": "topTwoPrimaryUnopposed",
                "firstName": "Juan",
                "middleName": "C.",
                "lastName": "Vargas",
                "suffix": None,
                "incumbent": True,
                "party": "dem",
            },
            "placeTwo": {
                "type": "topTwoPrimaryUnopposed",
                "firstName": "Juan",
                "middleName": "M",
                "lastName": "Hidalgo",
                "suffix": "Jr",
                "incumbent": False,
                "party": "gop",
            },
        },
        "VA-04": {
            "gop": {
              "type": "atConvention",
              "firstName": "Leon",
              "middleName": None,
              "lastName": "Benjamin",
              "suffix": None,
              "incumbent": False
            }
        },
        "VA-05": {
            "gop": {
              "type": "atConvention",
              "firstName": "Bob",
              "middleName": None,
              "lastName": "Good",
              "suffix": None,
              "incumbent": False
            }
        },
        "VA-06": {
          "dem": {
            "type": "atConvention",
            "firstName": "Nicholas",
            "middleName": None,
            "lastName": "Betts",
            "suffix": None,
            "incumbent": False
          }
        },
        "VA-07": {
          "gop": {
            "type": "atConvention",
            "firstName": "Nick",
            "middleName": None,
            "lastName": "Freitas",
            "suffix": None,
            "incumbent": False
          }
        },
        "VA-08": {
          "gop": {
            "type": "atConvention",
            "firstName": "Jeff",
            "middleName": None,
            "lastName": "Jordan",
            "suffix": None,
            "incumbent": False
          }
        },
        "VA-10": {
          "gop": {
            "type": "atConvention",
            "firstName": "Aliscia",
            "middleName": None,
            "lastName": "Andrews",
            "suffix": None,
            "incumbent": False
          }
        },
        "VA-11": {
          "gop": {
            "type": "atConvention",
            "firstName": "Manga",
            "middleName": None,
            "lastName": "Anantatmula",
            "suffix": None,
            "incumbent": False
          }
        },
        "AK-00": {
            "dem": {
              "type": "openDemPrimaryOutright",
              "firstName": "Alyse",
              "middleName": None,
              "lastName": "Galvin",
              "suffix": None,
              "incumbent": False,
              "margin": 68.78,
              "party": "ind"
            },
            "gop": {
              "type": "outright",
              "firstName": "Don",
              "middleName": None,
              "lastName": "Young",
              "suffix": None,
              "incumbent": True,
              "margin": 60.27
            },
        },
        "FL-02": {
          "dem": {"type": "nobody-ran"},
        },
        "FL-25": {
          "dem": {"type": "nobody-ran"},
        }
    },
    "senate": {
      "AK-SEN": {
        "dem": {
          "type": "openDemPrimaryOutright",
          "firstName": "Al",
          "middleName": None,
          "lastName": "Gross",
          "suffix": None,
          "incumbent": False,
          "margin": 64.08,
          "party": "ind"
        },
        "gop": {
          "type": "unopposed",
          "firstName": "Dan",
          "middleName": None,
          "lastName": "Sullivan",
          "suffix": None,
          "incumbent": True
        },
      },
    },
    "president": {
      "LA-POTUS": {
        "dem": {
          "type": "outright",
          "firstName": "Joe",
          "middleName": "",
          "lastName": "Biden",
          "suffix": "",
          "incumbent": False,
          "margin": 72.09
        },
        "gop": {
          "type": "outright",
          "firstName": "Donald",
          "middleName": "",
          "lastName": "Trump",
          "suffix": "",
          "incumbent": True,
          "margin": 94.27
        }
      },
    },
    "governor": {},
}
