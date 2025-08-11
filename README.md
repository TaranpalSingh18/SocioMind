# 🚀 **Growthzi AI Agent Backend**

## 📋 **Project Overview**
**Objective**: Build a backend system for an AI agent that creates and manages Facebook content for businesses. The agent simulates the capabilities of a smart social media manager: understand a business, stay updated on its industry, and generate lead-oriented posts that can be reviewed, edited, and published automatically.

## ✨ **Features**
- 🔍 **Business Understanding**: Analyze business websites and extract profiles
- 📰 **Industry News Analysis**: Stay updated on industry trends
- 🤖 **AI Content Generation**: Create engaging social media posts
- 📅 **Weekly Planning**: Schedule posts across the week
- 👁️ **Preview & Edit**: Review and modify content before publishing
- 📘 **Facebook Integration**: Connect and publish to Facebook pages

## 🏗️ **Architecture**
- **Backend**: Python + Flask
- **Validation**: Pydantic models for data validation
- **Modular Design**: Scalable and maintainable code structure

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- pip package manager

### **Installation**
```bash
# Clone the repository
git clone <your-repo-url>
cd growthzi

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

### **Server URL**
```
http://localhost:5000
```

---

## 📚 **API Documentation**

### **Base URL**
```
http://localhost:5000
```

---

### **1. Business Understanding API**
**Route**: `/business/extract`  
**Method**: `POST`  
**Route**: `/business/extract-get`
**Method**: `GET`   
**Description**: Analyzes a business website URL and extracts structured business profile information.

**Request Body**:
```json
{
  "url": "https://www.w3schools.com/howto/howto_website_restaurant.asp"
}
```

**Response**:
```json
{
  "industry": "Education",
  "name": "W3Schools",
  "services": [
    "Free Tutorials",
    "References",
    "Create a Website",
    "Exercises",
    "Quizzes",
    "Course",
    "Programs",
    "Web Development",
    "Introduction to Programming",
    "Code Editor",
    "Test Your Typing Speed",
    "Play a Code Game",
    "Cyber Security",
    "Accessibility",
    "Join our Newsletter",
    "Web Templates",
    "Web Statistics",
    "Web Certificates",
    "Web Development",
    "Create a Website (W3.CSS)",
    "Make a Website (BS3)",
    "Make a Website (BS4)",
    "Make a Website (BS5)",
    "Create and View a Website",
    "Create a Link Tree Website",
    "Create a Portfolio",
    "Create a Resume",
    "Make a Restaurant Website",
    "Make a Business Website",
    "Make a WebBook",
    "Center Website",
    "Contact Section",
    "About Page",
    "Big Header",
    "Example Website"
  ],
  "tone": "Informative"
}
```

---

### **2. Industry News Analyzer API**
**Route**: `/news/news`  
**Method**: `POST` 
**Route**: `/news/<keyword>`  
**Description**: Analyzes industry news and provides current headlines and insights.

**Request Body**:
```json
{
  "keywords": ["gym", "workout", "health"]
}
```

**Response**:
```json
{
  "news": [
    {
      "relevance_score": "High",
      "summary": "A new study has found that a specific exercise is the best for brain health, and it's not running.",
      "title": "Forget running - the best exercise for brain health has just been revealed in an incredible new study"
    },
    {
      "relevance_score": "High",
      "summary": "A person shares their experience of cutting their workouts in half and still seeing gains.",
      "title": "I Cut My Workouts in Half. The Gains Didn\u2019t Stop\u2014Here\u2019s Why"
    },
    {
      "relevance_score": "High",
      "summary": "Experts share their insights on how long it takes to transform your body in the gym.",
      "title": "How Long Does It Take To Transform Your Body In The Gym? The Answer Isn\u2019t What You Think"
    },
    {
      "relevance_score": "High",
      "summary": "Experts recommend a specific exercise for women over 50 to improve their health.",
      "title": "Experts Say This Is the One Exercise Every Woman Over 50 Should Be Doing"
    },
    {
      "relevance_score": "High",
      "summary": "Experts weigh in on the effectiveness of vibration plates for weight loss and strength gain.",
      "title": "Are Vibration Plates a Magic Bullet for Losing Weight and Gaining Strength? We Asked the Experts"
    }
  ]
}
```

---

### **3. Content Generator API**
**Route**: `/content/captions`  
**Method**: `POST`  
**Description**: Generates AI-powered post captions based on business profile and preferences.

**Request Body**:
```json
{
  "business_profile": {
    "name": "FitLife Gym",
    "industry": "Fitness & Wellness",
    "services": ["Personal Training", "Group Classes"],
    "tone": "professional"
  },
  "industry_news": {
    "news": [
      {
        "relevance_score": "high",
        "summary": "New fitness trends emerging",
        "title": "Fitness Industry Update"
      }
    ]
  },
  "tone": "professional",
  "post_type": "tip",
  "frequency": 5
}
```

**Response**:
```json
{
    "captions": [
        {
            "POST 1": "Here are 5 ready-to-publish post captions for FitLife Gym:"
        },
        {
            "POST 2": "1. Post 1: \nStay ahead of the fitness curve with our expert-led group classes! As the fitness industry continues to evolve, we're committed to providing you with the latest and greatest workouts to help you reach your goals. #FitnessIndustryUpdate #GroupFitness #Wellness"
        },
        {
            "POST 3": "2. Post 2: \nLooking for a personalized approach to fitness? Our certified trainers offer one-on-one personal training sessions tailored to your unique needs and goals. Stay on track and reach new heights with FitLife Gym's expert guidance. #PersonalTraining #FitnessMotivation #Wellness"
        },
        {
            "POST 4": "3. Post 3: \nNew year, new you! Kickstart your fitness journey with our special introductory offer. Limited time only, don't miss out on this opportunity to transform your body and mind. #FitnessGoals #NewYearNewYou #Wellness"
        },
        {
            "POST 5": "4. Post 4: \nWhat's trending in the fitness world? From high-intensity interval training (HIIT) to functional strength training, we're always on top of the latest trends to ensure our workouts stay fresh and exciting. Stay fit, stay fun with FitLife Gym! #FitnessTrends #Wellness #GroupFitness"
        },
        {
            "POST 6": "5. Post 5: \nInvest in yourself this week! Treat yourself to a FitLife Gym membership and unlock a world of fitness possibilities. From group classes to personal training, our expert team is here to support you every step of the way. #FitnessMembership #Wellness #PersonalGrowth"
        }
    ],
    "total_posts": 6
}
```

---

### **4. Weekly Planner API**
**Route**: `/post/week`  
**Method**: `POST`  
**Description**: Creates a weekly schedule with posts mapped to specific days.

**Request Body**:
```json
{
  "frequency": 5,
  "days": ["Monday", "Wednesday", "Friday"]
}
```

**Response**:
```json
{
    "message": "Weekly schedule created with 5 posts across 3 days",
    "success": true,
    "summary": {
        "days_with_posts": 3,
        "frequency_requested": 5,
        "preferred_days": [
            "Monday",
            "Wednesday",
            "Friday"
        ],
        "schedule_type": "Custom",
        "total_posts": 5
    },
    "weekly_schedule": {
        "Friday": [
            {
                "caption": "🚀 Transform your business with AI! Our latest automation solutions have helped clients increase productivity by 40%. Ready to join the AI revolution? Let's chat! #AIConsulting #BusinessAutomation #DigitalTransformation #TechSolutions #Innovation",
                "engagement_rate": 8.5,
                "platform": "LinkedIn",
                "post_id": "post_001",
                "post_type": "promotional",
                "scheduled_time": "09:00 AM"
            }
        ],
        "Monday": [
            {
                "caption": "⚡ BREAKING: Our AI-powered analytics tool just helped a client identify $50K in cost savings! Imagine what insights are hiding in your data. Ready to unlock them? 📊✨ #DataAnalytics #AIInsights #CostSavings #BusinessIntelligence #TechSolutions",
                "engagement_rate": 12.1,
                "platform": "LinkedIn",
                "post_id": "post_008",
                "post_type": "case_study",
                "scheduled_time": "08:30 AM"
            },
            {
                "caption": "🔥 Monday Motivation: Your body can stand almost anything. It's your mind you have to convince! Start this week strong with our HIIT class at 6 AM. First session FREE for new members! 💪 #MondayMotivation #HIITWorkout #FitnessGoals #NewMemberSpecial #FitLifeGym",
                "engagement_rate": 15.2,
                "platform": "Instagram",
                "post_id": "post_010",
                "post_type": "motivational",
                "scheduled_time": "05:45 AM"
            }
        ],
        "Wednesday": [
            {
                "caption": "✨ Friday Feature: Meet Sarah, a local bakery owner who transformed her business with our e-commerce solution! From 20 orders/week to 200+ orders/week in just 3 months. 🍰📈 What's stopping you from going digital? #ClientSuccess #EcommerceSolutions #DigitalTransformation #SmallBusiness #FridayFeature",
                "engagement_rate": 7.3,
                "platform": "Instagram",
                "post_id": "post_005",
                "post_type": "case_study",
                "scheduled_time": "03:45 PM"
            },
            {
                "caption": "📈 Market Monday: Interest rates dropped 0.25%! This could save buyers $200-300/month on a $400K home. Perfect time to make your move! Pre-approval letters available in 24 hours. Let's find your dream home! #MarketMonday #InterestRates #HomeBuying #PreApproval #DreamHome",
                "engagement_rate": 8.9,
                "platform": "LinkedIn",
                "post_id": "post_015",
                "post_type": "market_update",
                "scheduled_time": "11:00 AM"
            }
        ]
    }
}
```

---

### **5. Preview & Edit API**
**Route**: `/preview/view`  
**Method**: `GET`  
**Description**: Retrieves all scheduled posts for a week.

**Response**:
```json
[
  {
    "id": "post_001",
    "caption": "🚀 Transform your business with AI!...",
    "day": "Monday",
    "scheduledTime": "09:00 AM",
    "platform": "LinkedIn",
    "postType": "promotional",
    "isPublished": 1,
    "scheduled_this_week": 1
  }
]
```

**Route**: `/preview/edit/<post_id>`  
**Method**: `PUT`  
**Description**: Updates post content before publishing.

**Request Body**:
```json
"""suppose post_019 is to be edited.
/preview/edit/post_019
"""
{
  "caption": "Updated fitness journey content...",
  "scheduledTime": "10:00 AM",
  "platform": "LinkedIn"
}
```

**Response**:
```json
{
    "message": "Post updated successfully",
    "post": {
        "caption": "Updated fitness journey content...",
        "comments": 19,
        "day": "Thursday",
        "engagement_rate": 10.3,
        "id": "post_019",
        "isPublished": 1,
        "likes": 145,
        "platform": "LinkedIn",
        "postType": "behind_scenes",
        "scheduledTime": "10:00 AM",
        "scheduled_this_week": 0,
        "shares": 11
    },
    "updated_fields": [
        "caption",
        "scheduledTime",
        "platform"
    ]
}
```

**Route**: `/preview/delete/<post_id>`  
**Method**: `DELETE`  
**Description**: Removes scheduled post from publishing queue.


---

### **6. Facebook Page Connection API**
**Route**: `/facebook/connect`  
**Method**: `POST`  
**Description**: Simulates Facebook page connection.

**Request Body**:
```json
{
  "page_id": "123456789",
  "page_name": "My Business Page"
}
```

**Response**:
```json
[
  "message: Success",
  "Token: abc1234"
]
```

---



---

## 📁 **Project Structure**
```
growthzi/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── mockdata/
│   └── mock_post_data.py # Mock data for testing
├── models/
│   └── model.py          # Pydantic data models
└── routes/
    ├── business_api.py    # Business understanding API
    ├── content_api.py     # Content generation API
    ├── facebook.py        # Facebook integration API
    ├── news.py            # Industry news API
    ├── posts.py           # Weekly planner API
    ├── preview.py         # Preview & edit API
    └── testing.py         # Testing workflow API
```

---

## 🚨 **Error Handling**

The API includes comprehensive error handling for:
- Invalid JSON data
- Missing required fields
- Invalid frequency values
- Invalid day names
- Post not found errors
- Connection failures

All errors return appropriate HTTP status codes and descriptive error messages.

---

## 🔧 **Configuration**

### **Environment Variables**
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
FACEBOOK_ACCESS_TOKEN=your_facebook_token_here
GOOGLE_NEWS_API=your_google_news_api_key
```

### **CORS Configuration**
CORS is enabled by default to allow frontend access from browsers.

---

## 📝 **Testing Checklist**

- [ ] All 6 APIs respond correctly
- [ ] Business profile extraction works
- [ ] Industry news analysis returns relevant data
- [ ] Content generation creates appropriate captions
- [ ] Weekly planner distributes posts correctly
- [ ] Preview/edit functionality works
- [ ] Facebook connection simulation works
- [ ] Testing flow completes end-to-end
- [ ] Error handling works for invalid inputs

---

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📄 **License**

This project is part of the Growthzi Backend Developer Assignment.

---


## 🎯 **Next Steps**

- [ ] Implement real Facebook Graph API integration
- [ ] Add database persistence for posts and schedules
- [ ] Implement real-time content scheduling
- [ ] Add analytics and engagement tracking
- [ ] Create frontend dashboard for content management

---

**Happy Coding! 🚀**
