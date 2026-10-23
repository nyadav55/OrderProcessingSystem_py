# A Singleton ensures that a class has only one single instance throughout the entire lifecycle of your application. 
# No matter how many times you try to create a new object (e.g., Config()), 
# Python will always return the exact same object in memory.
# Goal: Ensure the application uses one shared configuration instance.

class AppConfig:
    """Stores shared application configuration."""
    _instance = None

    def __new__(cls):
    # 1. Check if an instance already exists
        if cls._instance is None:
            # 2. If it doesn't exist, create it using the parent object class
            cls._instance = super().__new__(cls)
        # 3. Return the single instance (either the newly created one or the existing one)
        return cls._instance

    def __init__(self):
        # 1. Check if this specific instance has already been setup before
        if not hasattr(self, "_initialized"):
            # 2. Set the default configuration settings
            self.environment = "development"
            self.currency = "USD"
            # 3. Mark the instance as initialized so this block never runs again
            self._initialized = True    

# Singleton Design Pattern (सिंगलटन डिज़ाइन पैटर्न) का एक बेहतरीन उदाहरण है।
# सिंगलटन पैटर्न का मुख्य उद्देश्य यह सुनिश्चित करना होता है कि पूरी एप्लीकेशन में उस क्लास का सिर्फ एक ही इंस्टेंस (Instance/Object) बने। 
# आप जितनी बार भी नया ऑब्जेक्ट बनाने की कोशिश करेंगे (जैसे: Config()), पायथन आपको हर बार मेमोरी में मौजूद वही पुराना ऑब्जेक्ट ही वापस करेगा।
# पायथन में ऑब्जेक्ट दो चरणों में बनता है: 
# __new__ (मेमोरी अलॉट करना) और __init__ (वैल्यू सेट करना- दोबारा वैल्यू बदलने से रोकना)। आइए दोनों को आसान शब्दों में समझते हैं: 

# __new__ मेथड पायथन का असली कंस्ट्रक्टर है। इसका काम नया ऑब्जेक्ट बनाना और उसे वापस (return) करना है।
# • cls._instance: यह क्लास के स्तर पर बना एक वेरिएबल होता है (जो शुरुआत में None होता है)। यह इकलौते ऑब्जेक्ट को संभाल कर रखता है।
# • super().__new__(cls): जब पहली बार कोड चलता है और कोई ऑब्जेक्ट नहीं होता, तब यह लाइन मेमोरी में नया ऑब्जेक्ट बनाती है। 
# अगली बार कॉल करने पर यह नया ऑब्जेक्ट बनाने के बजाय सीधे पुराना ऑब्जेक्ट ही वापस भेज देती है।

# __init__ मेथड का काम ऑब्जेक्ट में वैल्यू सेट (Initialize) करना है। 
# पायथन का नियम है कि आप जितनी बार भी ClassName() लिखेंगे, __init__ उतनी ही बार चलेगा। 
# क्योंकि __new__ हर बार पुराना ऑब्जेक्ट ही वापस कर रहा है, इसलिए __init__ हर बार उसकी पुरानी वैल्यू को मिटाकर नई वैल्यू सेट कर देगा। 
# इसी को रोकने के लिए नीचे दिया गया लॉजिक लगाया गया है:

# • hasattr(self, "_initialized"): यह चेक करता है कि क्या ऑब्जेक्ट के पास _initialized नाम का कोई वेरिएबल है।
# • पहली बार में: यह वेरिएबल नहीं मिलता, इसलिए if कंडीशन सच हो जाती है। सेटिंग्स (environment, currency) सेव होती हैं और _initialized = True हो जाता है।
# • दूसरी या तीसरी बार में: चूंकि ऑब्जेक्ट वही पुराना है, इसलिए उसके पास _initialized = True पहले से मौजूद होता है। if कंडीशन गलत हो जाती है, और कोड बिना आपकी सेटिंग्स को बदले चुपचाप बाहर आ जाता है।