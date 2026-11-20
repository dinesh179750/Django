from django.shortcuts import render


data= [
    {"name": "The Secrets", "chapters": 10, "amount": 300},
    {"name": "Bhagavad Gita", "chapters": 18, "amount": 399},
    {"name": "Ramayanam", "chapters": 7, "amount": 100},
    {"name": "Expression of Love", "chapters": 8, "amount": 299},
    {"name": "It Ends with Us", "chapters": 35, "amount": 400},
    {"name": "Wings of Fire", "chapters": 42, "amount": 250},
    {"name": "The Alchemist", "chapters": 12, "amount": 299},
    {"name": "Atomic Habits", "chapters": 20, "amount": 450},
    {"name": "Rich Dad Poor Dad", "chapters": 10, "amount": 350},
    {"name": "The Psychology of Money", "chapters": 20, "amount": 399},
    {"name": "Think and Grow Rich", "chapters": 15, "amount": 275},
    {"name": "Ikigai", "chapters": 9, "amount": 299},
    {"name": "Deep Work", "chapters": 15, "amount": 399},
    {"name": "The Power of Habit", "chapters": 9, "amount": 375},
    {"name": "The 5 AM Club", "chapters": 20, "amount": 425},
    {"name": "Zero to One", "chapters": 14, "amount": 350},
    {"name": "The Lean Startup", "chapters": 13, "amount": 499},
    {"name": "Start with Why", "chapters": 13, "amount": 399},
    {"name": "How to Win Friends and Influence People", "chapters": 30, "amount": 299},
    {"name": "The Subtle Art of Not Giving a F*ck", "chapters": 9, "amount": 350},
    {"name": "To Kill a Mockingbird", "chapters": 31, "amount": 399},
    {"name": "Pride and Prejudice", "chapters": 61, "amount": 299},
    {"name": "The Great Gatsby", "chapters": 9, "amount": 199},
    {"name": "1984", "chapters": 24, "amount": 250},
    {"name": "Animal Farm", "chapters": 10, "amount": 180},
    {"name": "The Hobbit", "chapters": 19, "amount": 450},
    {"name": "Harry Potter and the Philosopher's Stone", "chapters": 17, "amount": 499},
    {"name": "The Lord of the Rings", "chapters": 62, "amount": 699},
    {"name": "The Catcher in the Rye", "chapters": 26, "amount": 275},
    {"name": "Jane Eyre", "chapters": 38, "amount": 399},
    {"name": "Little Women", "chapters": 47, "amount": 350},
    {"name": "The Book Thief", "chapters": 88, "amount": 450},
    {"name": "The Fault in Our Stars", "chapters": 25, "amount": 299},
    {"name": "The Notebook", "chapters": 24, "amount": 275},
    {"name": "Me Before You", "chapters": 29, "amount": 350},
    {"name": "The Kite Runner", "chapters": 25, "amount": 399},
    {"name": "A Thousand Splendid Suns", "chapters": 51, "amount": 425},
    {"name": "Life of Pi", "chapters": 100, "amount": 450},
    {"name": "The Da Vinci Code", "chapters": 105, "amount": 499},
    {"name": "Angels and Demons", "chapters": 137, "amount": 450},
    {"name": "Sherlock Holmes", "chapters": 12, "amount": 299},
    {"name": "The Silent Patient", "chapters": 34, "amount": 399},
    {"name": "Gone Girl", "chapters": 55, "amount": 425},
    {"name": "The Girl on the Train", "chapters": 40, "amount": 350},
    {"name": "Murder on the Orient Express", "chapters": 27, "amount": 275},
    {"name": "The Hunger Games", "chapters": 27, "amount": 399},
    {"name": "Divergent", "chapters": 39, "amount": 350},
    {"name": "The Maze Runner", "chapters": 62, "amount": 399},
    {"name": "Sapiens", "chapters": 20, "amount": 499},
    {"name": "A Brief History of Time", "chapters": 12, "amount": 399}
]
std=[
    {"name":'dinesh',"gender":'male'},
    {"name":'raju',"gender":'male'},
    {"name":'sreeja',"gender":'female'},
    {"name":'karthik',"gender":'male'},
    {"name":'maha',"gender":'female'},
    {"name":'mamatha',"gender":'female'},
]
books = [
    {
        "id": 1,
        "bookname": "The Silent River Vol 1",
        "author": "Arun Mehta",
        "price": 299,
        "category": "Fiction",
        "total_chapters": 12,
        "books_in_store": 40,
        "description": "The Silent River Vol 1 by Arun Mehta is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 2,
        "bookname": "Data Science Essentials Vol 2",
        "author": "Priya Sharma",
        "price": 499,
        "category": "Education",
        "total_chapters": 15,
        "books_in_store": 25,
        "description": "Data Science Essentials Vol 2 by Priya Sharma is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 3,
        "bookname": "Winds of Change Vol 3",
        "author": "Ravi Kumar",
        "price": 350,
        "category": "Drama",
        "total_chapters": 10,
        "books_in_store": 30,
        "description": "Winds of Change Vol 3 by Ravi Kumar is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 4,
        "bookname": "Python for Everyone Vol 4",
        "author": "Sneha Reddy",
        "price": 450,
        "category": "Technology",
        "total_chapters": 20,
        "books_in_store": 50,
        "description": "Python for Everyone Vol 4 by Sneha Reddy is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 5,
        "bookname": "The Forgotten Temple Vol 5",
        "author": "Kiran Das",
        "price": 399,
        "category": "Adventure",
        "total_chapters": 18,
        "books_in_store": 22,
        "description": "The Forgotten Temple Vol 5 by Kiran Das is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 6,
        "bookname": "Mindful Living Vol 6",
        "author": "Ananya Rao",
        "price": 275,
        "category": "Self-help",
        "total_chapters": 9,
        "books_in_store": 35,
        "description": "Mindful Living Vol 6 by Ananya Rao is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 7,
        "bookname": "SQL Mastery Vol 7",
        "author": "Vikram Singh",
        "price": 520,
        "category": "Education",
        "total_chapters": 14,
        "books_in_store": 28,
        "description": "SQL Mastery Vol 7 by Vikram Singh is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 8,
        "bookname": "Echoes of the Past Vol 8",
        "author": "Meera Iyer",
        "price": 310,
        "category": "Historical Fiction",
        "total_chapters": 11,
        "books_in_store": 18,
        "description": "Echoes of the Past Vol 8 by Meera Iyer is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 9,
        "bookname": "The Startup Journey Vol 9",
        "author": "Rahul Verma",
        "price": 600,
        "category": "Business",
        "total_chapters": 16,
        "books_in_store": 20,
        "description": "The Startup Journey Vol 9 by Rahul Verma is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 10,
        "bookname": "Ocean Whispers Vol 10",
        "author": "Lakshmi Menon",
        "price": 280,
        "category": "Poetry",
        "total_chapters": 8,
        "books_in_store": 15,
        "description": "Ocean Whispers Vol 10 by Lakshmi Menon is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 11,
        "bookname": "AI Revolution Vol 11",
        "author": "Suresh Patil",
        "price": 700,
        "category": "Technology",
        "total_chapters": 22,
        "books_in_store": 40,
        "description": "AI Revolution Vol 11 by Suresh Patil is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 12,
        "bookname": "The Healing Touch Vol 12",
        "author": "Divya Nair",
        "price": 320,
        "category": "Health",
        "total_chapters": 12,
        "books_in_store": 27,
        "description": "The Healing Touch Vol 12 by Divya Nair is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 13,
        "bookname": "Journey to the Stars Vol 13",
        "author": "Ajay Pillai",
        "price": 450,
        "category": "Science",
        "total_chapters": 19,
        "books_in_store": 33,
        "description": "Journey to the Stars Vol 13 by Ajay Pillai is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 14,
        "bookname": "The Art of Negotiation Vol 14",
        "author": "Neha Kapoor",
        "price": 380,
        "category": "Business",
        "total_chapters": 13,
        "books_in_store": 21,
        "description": "The Art of Negotiation Vol 14 by Neha Kapoor is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 15,
        "bookname": "Mystic Hills Vol 15",
        "author": "Rohan Das",
        "price": 299,
        "category": "Fantasy",
        "total_chapters": 17,
        "books_in_store": 26,
        "description": "Mystic Hills Vol 15 by Rohan Das is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 16,
        "bookname": "Cooking with Love Vol 16",
        "author": "Shalini Gupta",
        "price": 340,
        "category": "Cooking",
        "total_chapters": 12,
        "books_in_store": 19,
        "description": "Cooking with Love Vol 16 by Shalini Gupta is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 17,
        "bookname": "The Hidden Truth Vol 17",
        "author": "Manoj Reddy",
        "price": 410,
        "category": "Thriller",
        "total_chapters": 14,
        "books_in_store": 24,
        "description": "The Hidden Truth Vol 17 by Manoj Reddy is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 18,
        "bookname": "Gardening Made Easy Vol 18",
        "author": "Pooja Desai",
        "price": 360,
        "category": "Lifestyle",
        "total_chapters": 11,
        "books_in_store":"en Truth Vol 17 by Manoj Reddy is a thoughtfully written book th"
    },
    {
        "id": 23,
        "bookname": "Voices of Freedom Vol 23",
        "author": "Tanvi Rao",
        "price": 420,
        "category": "History",
        "total_chapters": 15,
        "books_in_store": 32,
        "description": "Voices of Freedom Vol 23 by Tanvi Rao is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 24,
        "bookname": "Creative Writing Guide Vol 24",
        "author": "Deepak Malhotra",
        "price": 360,
        "category": "Education",
        "total_chapters": 12,
        "books_in_store": 29,
        "description": "Creative Writing Guide Vol 24 by Deepak Malhotra is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 25,
        "bookname": "Digital Horizons Vol 25",
        "author": "Nisha Bhat",
        "price": 510,
        "category": "Technology",
        "total_chapters": 20,
        "books_in_store": 41,
        "description": "Digital Horizons Vol 25 by Nisha Bhat is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 26,
        "bookname": "Beyond the Clouds Vol 26",
        "author": "Karthik Iyer",
        "price": 330,
        "category": "Fiction",
        "total_chapters": 11,
        "books_in_store": 23,
        "description": "Beyond the Clouds Vol 26 by Karthik Iyer is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 27,
        "bookname": "Secrets of the Forest Vol 27",
        "author": "Sonia Jain",
        "price": 370,
        "category": "Adventure",
        "total_chapters": 14,
        "books_in_store": 28,
        "description": "Secrets of the Forest Vol 27 by Sonia Jain is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 28,
        "bookname": "Infinite Dreams Vol 28",
        "author": "Arvind Joshi",
        "price": 400,
        "category": "Fantasy",
        "total_chapters": 16,
        "books_in_store": 34,
        "description": "Infinite Dreams Vol 28 by Arvind Joshi is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 29,
        "bookname": "The Last Kingdom Vol 29",
        "author": "Tanvi Rao",
        "price": 450,
        "category": "Historical Fiction",
        "total_chapters": 18,
        "books_in_store": 30,
        "description": "The Last Kingdom Vol 29 by Tanvi Rao is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 30,
        "bookname": "Code Warriors Vol 30",
        "author": "Sneha Reddy",
        "price": 520,
        "category": "Technology",
        "total_chapters": 21,
        "books_in_store": 39,
        "description": "Code Warriors Vol 30 by Sneha Reddy is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 31,
        "bookname": "Future of Finance Vol 31",
        "author": "Rahul Verma",
        "price": 580,
        "category": "Business",
        "total_chapters": 17,
        "books_in_store": 27,
        "description": "Future of Finance Vol 31 by Rahul Verma is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 32,
        "bookname": "Whispers in the Dark Vol 32",
        "author": "Neha Kapoor",
        "price": 310,
        "category": "Thriller",
        "total_chapters": 12,
        "books_in_store": 22,
        "description": "Whispers in the Dark Vol 32 by Neha Kapoor is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 33,
        "bookname": "The Eternal Flame Vol 33",
        "author": "Ajay Pillai",
        "price": 390,
        "category": "Fantasy",
        "total_chapters": 15,
        "books_in_store": 31,
        "description": "The Eternal Flame Vol 33 by Ajay Pillai is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 34,
        "bookname": "Building Blocks of Web Vol 34",
        "author": "Priya Sharma",
        "price": 470,
        "category": "Education",
        "total_chapters": 19,
        "books_in_store": 36,
        "description": "Building Blocks of Web Vol 34 by Priya Sharma is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 35,
        "bookname": "Shadows of Time Vol 35",
        "author": "Ravi Kumar",
        "price": 320,
        "category": "Drama",
        "total_chapters": 11,
        "books_in_store": 25,
        "description": "Shadows of Time Vol 35 by Ravi Kumar is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 36,
        "bookname": "The Innovator’s Mind Vol 36",
        "author": "Suresh Patil",
        "price": 650,
        "category": "Technology",
        "total_chapters": 22,
        "books_in_store": 42,
        "description": "The Innovator’s Mind Vol 36 by Suresh Patil is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 37,
        "bookname": "Healing Through Nature Vol 37",
        "author": "Divya Nair",
        "price": 340,
        "category": "Health",
        "total_chapters": 13,
        "books_in_store": 29,
        "description": "Healing Through Nature Vol 37 by Divya Nair is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 38,
        "bookname": "Stars Beyond Reach Vol 38",
        "author": "Ajay Pillai",
        "price": 480,
        "category": "Science",
        "total_chapters": 18,
        "books_in_store": 34,
        "description": "Stars Beyond Reach Vol 38 by Ajay Pillai is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 39,
        "bookname": "Negotiation Secrets Vol 39",
        "author": "Neha Kapoor",
        "price": 370,
        "category": "Business",
        "total_chapters": 14,
        "books_in_store": 26,
        "description": "Negotiation Secrets Vol 39 by Neha Kapoor is a thoughtfully written book that explores ideas, characters, and themes with depth, offering readers knowledge, entertainment, and inspiration through engaging storytelling and practical insights."
    },
    {
        "id": 40,
        "bookname": "Fantasy Realms Vol 40",
        "author": "Rohan Das",
        "price": 310,
        "category": "Fantasy",
        "total_chapters": 16,
        "books_in_store": 28,
        "description": "Fantasy Realms Vol 40 by Rohan Das is a thoughtfully written book that explores ideas, characters, and themes with depth, offering.and"
    }
]

def home(request):
    context={
        "books":data
    }
    return render(request,'index.html',context)

def student(request):
    context={
        "data":std
    }
    return render(request,'student.html',context)
def book_store(request):
    context={
        "sap":books
    }
    return render(request,'book_store.html',context)