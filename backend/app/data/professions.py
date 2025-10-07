# app/data/professions.py

PROFESSIONS_BY_NUMBER = {
    1: [
        "CEO", "MD", "Chairman", "Army", "Commander", "Fire Officer", "Luxury and Glamour",
        "Boiler", "Restaurants", "Glass Factory", "Government Top Positions", "Goldsmith",
        "Government Tenders", "HOD", "Politics", "Solar Plant", "Power and Electricity",
        "Heat", "Gobar Gas", "Administrative Jobs", "Operational Jobs"
    ],
    2: [
        "Milk Products", "Coffee", "Ice Cream", "Agriculture", "Food", "Grains", "Mineral Water Plant",
        "Pepsi", "Coke", "Thumbs Up", "Dairy Plant", "Chemical", "Wine Shop", "Medical Shop",
        "Housekeeping", "Painting", "Dentist"
    ],
    3: [
        "Teaching", "Training", "Education", "Advertising", "Coaching", "Yoga Teacher", "Play School",
        "Stationery", "Book Shop", "Library", "Newspaper", "Publishing House", "Singer", "Music",
        "Art Work", "Anchor", "School", "College", "Healing", "Spiritual", "Research", "Counselling",
        "Occult", "Journalism", "Story Writer", "Meditation", "Blogger", "Sales Marketing"
    ],
    4: [
        "Law", "Hacking", "Government Sector", "Police", "IT", "Advisory Positions", "Army", "Navy",
        "Bouncer", "Security Services", "Camera", "CCTV", "Sales", "Marketing", "Digital Marketing",
        "E-commerce", "Arguments", "Handcraft", "Chef", "Politics", "AI", "RAW", "Sports"
    ],
    5: [
        "Real Estate", "Financial Services", "Computer Work", "Teaching", "Banking", "Data Entry",
        "IT Services", "Referee", "Agriculture", "Property Work", "Doctor", "CA"
    ],
    6: [
        "Hotel", "Tour and Travels", "Air Hostess", "Designers", "Acting", "Choreography", "Bar",
        "Disco", "Modelling", "Beauty", "Salons", "Makeup Artist", "Cosmetics", "Garments", "Boutique",
        "Media", "Crockery", "Event Management", "Car Showroom", "Real Estate", "Jewellery",
        "Liquor Shops", "Theatres", "Dancers"
    ],
    7: [
        "Occult", "Music", "Teaching", "Education", "Doctor", "Foreign Language", "Cyber Crime",
        "Medicine", "PhD", "Research", "Scientists", "Healing", "CID", "CGI", "Spiritual", "Detectives",
        "RAW", "Spy", "CCTV", "Software Developer", "Counsellor", "Astrology"
    ],
    8: [
        "Law", "Dance", "Press", "Shoes", "Hardware", "Iron", "Finance", "CA", "Transport",
        "Car Showroom", "Automobiles", "Service Stations", "Coal Mines", "Printing", "Electronics",
        "Discipline", "Civil Engineering", "Manufacturing", "Mechanics", "Gym", "Yoga", "Construction",
        "Car Rental", "Junkyard", "Builder"
    ],
    9: [
        "Army", "Surgeons", "Police", "Navy", "Sports", "Gym", "Workouts", "IPS", "PCS", "Chef",
        "NGO", "Charity", "Physiotherapist", "Healing", "Doctor", "Blood Bank", "Surgical Instruments",
        "Medicine"
    ]
}

FRIEND_ENEMY_NEUTRAL = {
    1: {"friends": [9, 2, 5, 3, 6, 1], "enemies": [8], "neutral": [4, 7]},
    2: {"friends": [1, 5, 3, 2], "enemies": [8, 4, 9], "neutral": [6, 7]},
    3: {"friends": [1, 5, 3], "enemies": [6], "neutral": [7, 4, 8, 9, 2]},
    4: {"friends": [7, 1, 5, 6], "enemies": [2, 9, 4, 8], "neutral": [3]},
    5: {"friends": [1, 2, 3, 6, 5], "enemies": [], "neutral": [4, 7, 8, 9]},
    6: {"friends": [1, 7, 4, 6, 5], "enemies": [3], "neutral": [2, 8, 9]},
    7: {"friends": [4, 6, 1, 5, 3], "enemies": [], "neutral": [2, 3, 8, 9, 7]},
    8: {"friends": [5, 3], "enemies": [1, 2, 4, 8], "neutral": [9, 6, 7]},
    9: {"friends": [1, 5], "enemies": [2, 4, 9], "neutral": [3, 7, 6, 8]},
}

ANTI_PAIRS = {(1, 8), (8, 1), (2, 8), (8, 2), (3, 6), (6, 3)}