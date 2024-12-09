import streamlit as st
from openai import OpenAI
import re

st.title("Qitaf Virtual Assistant")
st.markdown("Ask questions about STC's Qitaf loyalty program in **Arabic** or **English**.")

# CSS for RTL support
st.markdown("""
    <style>
        .rtl {
            direction: rtl;
            text-align: right;
        }
        .ltr {
            direction: ltr;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

def is_arabic(text):
    # Pattern to match Arabic characters
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')
    return bool(arabic_pattern.search(text))

def display_message_with_direction(message):
    direction_class = "rtl" if is_arabic(message) else "ltr"
    st.markdown(f'<div class="{direction_class}">{message}</div>', unsafe_allow_html=True)

# Define the prompt with FAQs and partner data
def generate_qitaf_prompt():
    faqs = """
    ### FAQs:
    -1ما هو برنامج قطاف؟ 
    قطاف هو برنامج الولاء المقدم من stc نقدم عروضًا وخصومات حصرية لجميع العملاء داخل وخارج الشبكة.
    -2كيف يمكنني التسجيل في برنامج قطاف؟
    يمكنك التسجيل عن طريق إرسال 201 إلى 900، أو من خلال تطبيق mystc 
    -3 من هم المؤهلون للانضمام إلى برنامج قطاف؟ 
    جميع عملاء stc يمكنهم الانضمام إلى برنامج قطاف، باستثناء العملاء المدرجين في قائمة الديون، فلا يمكنهم التسجيل في البرنامج.
    -4هل يمكنني تسجيل جميع أرقامي في قطاف؟
    نعم، عند التسجيل في برنامج قطاف، سيتم إضافة جميع أرقامك إلى العضوية المرتبطة برقم الهوية، وستبدأ حسبة النقاط 
    -5كيف يمكنني كسب نقاط قطاف؟
    يمكنك التسجيل في برنامج قطاف والبدء في كسب النقاط عند دفع الفواتير أو عند شحن رصيد رقم سوا، واستبدال النقاط بمجموعة من المكافآت، سواء مكافآت داخلية مثل الدقائق، الرسائل، أو البيانات المحلية والتجوال الدولي، بالإضافة إلى مكافآت خارجية عبر شركاء قطاف.
    -6متى سأستلم النقاط المكتسبة؟
    ستتلقى إشعارًا برسالة نصية فور كسب النقاط، سواء عند دفع الفاتورة مع stc أو لدى شركاء كسب النقاط في قطاف. لمعرفة المزيد عن شركاء الكسب، اضغط هنا.
    -7كم عدد النقاط التي سأكسبها مقابل دفع الفواتير؟
    مقابل كل 15 ريال مدفوع يحصل العميل على:
    •	عملاء كلاسيك وتميز الذهبي: نقطة واحدة.
    •	عملاء تميز البلاتيني: 1.5 نقطة.
    •	عملاء تميز الماسي: نقطتين.
    -8ما هي التكاليف والباقات المستثناة من كسب نقاط قطاف؟
    تشمل المبالغ التالية: (ضريبة القيمة المضافة - تقسيط الأجهزة - خدمات الدفع المباشر - باقات التجوال - بعض الخدمات الإضافية - بعض باقات الدفع الآجل القديمة). لمزيد من المعلومات، يرجى زيارة صفحة الأسئلة الشائعة.
    -9من هم المؤهلون لكسب نقاط قطاف؟
    عملاء المفوتر، الثابت، سوا و عملاء المشغلين الآخرين غير المنتمين إلى stc
    -10كيف يكسب عملاء الدفع المسبق نقاط قطاف؟
    عن طريق شحن رصيد سوا.
    -11كيف يكسب عملاء الدفع الآجل نقاط قطاف؟
    عند دفع الفواتير.
    -12كيف يكسب عملاء المشغلين الآخرين غير  stcنقاط قطاف؟
    عند التسوق مع شركائنا أو تحويل النقاط من برامج ولاء أخرى إلى قطاف.
    -13 هل سأكسب نقاط قطاف عند دفع فواتير باقة جوال 45؟
    لا، لن تكسب نقاط قطاف عند دفع الاشتراك الأساسي لهذه الباقة، ولكن ستكسب نقاطًا على المبالغ الإضافية المدفوعة التي تخضع لقواعد احتساب نقاط قطاف.
    -14 هل سأكسب نقاط قطاف عند دفع فواتير باقة جوال 25؟
    لا، لن تكسب نقاط قطاف عند دفع الاشتراك الأساسي لهذه الباقة، ولكن ستكسب نقاطًا على المبالغ الإضافية المدفوعة التي تخضع لقواعد احتساب نقاط قطاف.
    -15هل سأكسب نقاط قطاف عند دفع فواتير باقة الصفر؟
    لا، لن تكسب نقاط قطاف عند دفع الاشتراك الأساسي لهذه الباقة، ولكن ستكسب نقاطًا على المبالغ الإضافية المدفوعة التي تخضع لقواعد احتساب نقاط قطاف.
    -16هل سأكسب نقاط قطاف عند دفع فواتير باقة الصفر بلس؟
    لا، لن تكسب نقاط قطاف عند دفع الاشتراك الأساسي لهذه الباقة، ولكن ستكسب نقاطًا على المبالغ الإضافية المدفوعة التي تخضع لقواعد احتساب نقاط قطاف.
    -17ما هو منتج دفع الفواتير لعملاء المفوتر؟

    يسمح لك كعميل بتعديل مبلغ الفاتورة باستخدام نقاط قطاف لفواتير الهاتف الثابت والجوال.
    18- ما هو منتج دفع الفواتير للهاتف الثابت؟
    يسمح لك كعميل بتعديل مبلغ الفاتورة باستخدام نقاط قطاف لفواتير الهاتف الثابت والجوال.
    19- من يمكنه الاستفادة من هذه الخدمة؟
    عملاء المفوتر، الهاتف الثابت، و سوا المسجلين في قطاف.
    20- متى يتم تعديل المبلغ المسترد على الفاتورة؟
    إذا كانت فاتورة العميل بتاريخ 1 فبراير 2021 وقام باسترداد نقاط في 20 يناير 2021، سيتم تقليل المبلغ المستحق في فاتورة 1 فبراير 2021 بقيمة النقاط المستردة.
    21- ما هو منتج شحن الرصيد القابل للاسترداد؟
    يسمح لعملاء سوا باستخدام نقاط قطاف للحصول على رصيد.
    22- متى يتم الحصول على الرصيد بعد الاسترداد؟
    فورًا بعد عملية الاستبدال الناجحة.
    23- هل يمكن استخدام الرصيد المسترد لأي غرض؟
    نعم، يمكن استخدامه كرصيد سوا عادي.
    24- هل يمكن لباقات الدفع الآجل الأخرى الاستفادة من المكافآت في تطبيق mystc؟
    عند الدخول إلى قسم مكافآت قطاف في التطبيق، يتم تحديد رقم الجوال لعرض أنواع المكافآت المتاحة.
    25- هل يمكن الاستفادة من هذه الخدمة أكثر من مرة في الشهر؟
    لا، يمكن الاستفادة من هذا النوع من المكافآت مرة واحدة خلال الشهر.
    26- كيف يمكنني الاستفادة من نقاط قطاف؟
    •	دفع الفواتير أو شحن رصيد سوا.
    •	استبدال خدمات stc مثل (المكالمات المحلية - التجوال - الباقات - الرسائل الدولية).
    •	دفع فواتير الكهرباء.
    •	حجز تذاكر السينما.
    •	تحويل النقاط إلى أميال الفرسان.
    •	استبدال النقاط لدى تطبيقات السفر والتسوق.
    •	حجز تذاكر فعاليات موسم الرياض.
    •	زيارة العيادات الطبية باستخدام النقاط.
    27- ما هي خدمة شراء نقاط قطاف؟
    تتيح الخدمة لعملاء سوا ومفوتر زيادة نقاط قطاف بشراء نقاط إضافية.
    28- ما هي تكلفة نقاط قطاف؟
    تكلفة كل نقطة هي 0.30 ريال سعودي (دون ضريبة القيمة المضافة).
    29- كيف يمكن الاستفادة من شراء نقاط قطاف؟
    يمكن للعملاء شراء النقاط عبر تطبيق قطاف أو mystc.
    30- كيف يمكنني الدفع باستخدام نقاط قطاف إذا كنت من مشغل آخر؟
    يمكنك استخدام النقاط مع شركاء قطاف عبر تقديم رقم الجوال المسجل واستلام رمز التحقق OTP لإتمام الدفع.
    31- كيف يمكنني التحقق من رصيد نقاط قطاف إذا كنت من مشغل آخر؟
    يمكنك التحقق من رصيدك عبر تحميل تطبيق قطاف وزيارة الصفحة الرئيسية.
    32- كيف يمكنني التسجيل في قطاف إذا كنت من مشغل آخر؟
    يمكنك التسجيل عبر تطبيق قطاف أو زيارة الرابط التالي:
    التسجيل في قطاف
    أو زيارة أحد شركاء قطاف وتقديم رقم الجوال للتسجيل. ستتلقى رابط تسجيل عبر رسالة نصية لإكمال العملية.

    """

    partners = """
    ### Earn & Redeem Partners:
    - Water: berain (Earn: 5.0 points per 1 SAR spent, Redeem: 20.0 SAR spend to redeem 1 point), 
    - Insurance: Tawuniya (Earn: NA, Redeem: 10.0 SAR spend to redeem 1 point), TAMEENI (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    - Petroleum services: SASCO (Earn: 5.0 points per 1 SAR spent, Redeem: 15.0 SAR spend to redeem 1 point), Aldrees (Earn: 5.0 points per 1 SAR spent, Redeem: NA), Almahata (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    - Food delivery: Jahez (Earn: 5.0 points per 1 SAR spent, Redeem: 24.0 SAR spend to redeem 1 point), 
    - Technology: Rasan Information Technology Company (Earn: NA, Redeem: 20.0 SAR spend to redeem 1 point), 
    - Travel: Flyin (Earn: 5.0 points per 1 SAR spent, Redeem: 20.0 SAR spend to redeem 1 point), Daleel (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), trips (Earn: NA, Redeem: 15.0 SAR spend to redeem 1 point), AlFursan (Earn: 5.0 points per 1 SAR spent, Redeem: NA), Al Mosafer Travel & Tourism (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    - Gym: Fitness Time (Earn: 5.0 points per 1 SAR spent, Redeem: 20.0 SAR spend to redeem 1 point), 
    - Grocery: Nana (Earn: 5.0 points per 1 SAR spent, Redeem: 20.0 SAR spend to redeem 1 point), 
    - F&B: baja (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), 
    - Perfume: DERAAH (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Abdul Samad Al Qurashi (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Arabian Oud (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), OUD ELITE (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Arabian Luxury Gift Company (Earn: 5.0 points per 1 SAR spent, Redeem: NA), TWO MARK (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    - Car rental: Key Rent a Car (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Theeb (Earn: 5.0 points per 1 SAR spent, Redeem: 20.0 SAR spend to redeem 1 point), Lumi (Earn: NA, Redeem: 10.0 SAR spend to redeem 1 point), telgani (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Yelo Rent A Car (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), 
    - Egift: LikeCard (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), resal (Earn: 5.0 points per 1 SAR spent, Redeem: 20.0 SAR spend to redeem 1 point), YouGotAGift.com (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), 
    - Retail: nice (Earn: 5.0 points per 1 SAR spent, Redeem: 20.0 SAR spend to redeem 1 point), Al Sannat For Luggage (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Alshaya Watches (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Paris Gallery (Earn: 5.0 points per 1 SAR spent, Redeem: 20.0 SAR spend to redeem 1 point), the store (Earn: NA, Redeem: 20.0 SAR spend to redeem 1 point), Jarir (Earn: 5.0 points per 1 SAR spent, Redeem: NA), Jarir (Earn: 10.0 points per 1 SAR spent, Redeem: NA), SACO (Earn: 5.0 points per 1 SAR spent, Redeem: NA), Chalhoub Group Arabia (Earn: 5.0 points per 1 SAR spent, Redeem: NA), Apparel Company (Earn: 5.0 points per 1 SAR spent, Redeem: NA), Alshaya (Earn: 5.0 points per 1 SAR spent, Redeem: NA), Al Rugaib Furniture (Earn: 5.0 points per 1 SAR spent, Redeem: NA), Radwa Trading Company (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    - Electronics: SONY (Earn: 5.0 points per 1 SAR spent, Redeem: 20.0 SAR spend to redeem 1 point), YORK Air Conditioning (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Virgin MegaStore (Earn: 5.0 points per 1 SAR spent, Redeem: 20.0 SAR spend to redeem 1 point), STC Channels (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    - Entertainment: Toys R Us (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), QiDZ (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), VOX Cinema (Earn: 5.0 points per 1 SAR spent, Redeem: NA), stc tv (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    - Optical: MAGRABi (Earn: 5.0 points per 1 SAR spent, Redeem: 15.0 SAR spend to redeem 1 point), Al Maha Opticals (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Al Barakat Group (Earn: 5.0 points per 1 SAR spent, Redeem: 20.0 SAR spend to redeem 1 point), Mugla Optical (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Al Jamil Optical (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Toroun Optical (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), 
    - Beauty: NICE ONE (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), 
    - Fashion: Sayyar Trading Company (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), femi9 (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), L’Occitane Arabia for Trading Co. (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    - Health & wellness: MooveToHealth (Earn: NA, Redeem: 10.0 SAR spend to redeem 1 point), 9Round (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    - Flower: Spring Rose (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), 
    - Booking: Gathern (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Booking.com (Earn: NA, Redeem: 10.0 SAR spend to redeem 1 point), Rehlat (Earn: NA, Redeem: 10.0 SAR spend to redeem 1 point), webook (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    - Sweets: AANI & DANI (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Saadeddin Pastry (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Anoosh (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Giordano (Earn: 5.0 points per 1 SAR spent, Redeem: 20.0 SAR spend to redeem 1 point), Patchi (Earn: 5.0 points per 1 SAR spent, Redeem: NA), Dunkin Donuts (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    - Medical: CURA (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Al Farabi Medical Company (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Sanar Trading Company (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Bin Rushd Ophthalmic Center (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Children with Disability Association (Earn: 5.0 points per 1 SAR spent, Redeem: NA), TruDoc (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    - F&B Company: Arabian Entertainment Company (Earn: 5.0 points per 1 SAR spent, Redeem: 10.0 SAR spend to redeem 1 point), Hospitality Board Holding Company (Earn: NA, Redeem: 10.0 SAR spend to redeem 1 point), ALFA CO for Operations Services (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    - Advertising: ALSAAD Advertising Co. (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    - Pharmacy: Al Dawaa Pharmacies (Earn: 5.0 points per 1 SAR spent, Redeem: NA), nahdi (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    - Restaurant: Domino's Pizza (Earn: 5.0 points per 1 SAR spent, Redeem: NA), MAESTRO PIZZA (Earn: 5.0 points per 1 SAR spent, Redeem: NA), Kudu (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    - Charity: Ehsan (Earn: 5.0 points per 1 SAR spent, Redeem: NA), Jood Eskan (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    - Supermarket: Panda (Earn: 5.0 points per 1 SAR spent, Redeem: NA), Abdullah AlOthaim Markets (Earn: 5.0 points per 1 SAR spent, Redeem: NA), Tamimi Markets (Earn: 5.0 points per 1 SAR spent, Redeem: NA), Carrefour (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    - Bank: Saudi Digital Payments Company (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    - Utilities: Saudi Electricity Company (Earn: 10.0 points per 1 SAR spent, Redeem: NA), 
    - Aggregator: sela (Earn: 5.0 points per 1 SAR spent, Redeem: NA), 
    """
    return f"You are a virtual assistant for stc's Qitaf loyalty program. Respond to questions in Arabic or English based on the user's input language. If the information is not in the provided context, reply by saying you don't know the answer. \n\n{faqs}\n\n{partners}"

# Initialize OpenAI client with direct API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history with system message
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": generate_qitaf_prompt()}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":  # Skip displaying system message
        with st.chat_message(message["role"]):
            display_message_with_direction(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a question about Qitaf..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        display_message_with_direction(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        
        # Custom streaming display to handle RTL
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                direction_class = "rtl" if is_arabic(full_response) else "ltr"
                message_placeholder.markdown(f'<div class="{direction_class}">{full_response}</div>', 
                                          unsafe_allow_html=True)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})