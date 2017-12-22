#
version = "1.1"


# Answer choices (lowercase)
choices = ["çok olumlu", "olumlu", "kararsız", "olumsuz", "çok olumsuz"]


# Directory tree
temp_dir = "Temp" 
csv_dir = "CSV_Files" 
pdf_dir = "PDF_Files"
log_dir = "Logs"
zip_dir = "ZIP_Files"
db_dir = "Databases"
user_dir = "User_Files"
archieve_dir = "Archive"
fig_path = None # Latex'in figure klasorunu bulmasi icin


# Activate debug mode (Bool):
debug = False


# Plot colors:
colors = [(0,1,0),(1,1,0),"cyan","orange",(1,0,0)]


# Pie and Bar graph settings:
scale_pie = 1
scale_bar = 0.6
#
font_pie = 12
font_bar = 16
#
figsize_pie = [4,3]
figsize_bar = [5,3]
#
pie_pct_limit = 1


# Doc Properties:
geometry = {
            "top":"2cm",
            "left":"1.5cm",
            "right":"1.5cm",
            "bottom":"2cm",
            "includeheadfoot": False
            }


# Eliminate all negative comments (Bool):
eliminate = True
eliminate_choice = choices[-1] 


# Database Specific Variables DO NOT CHANGE:
db_name = "eem_erciyes.db"
db = None
cursor = None


# Logger:
log_file = "main_log.txt"
logger = None


# SMTP Server Settings:
smtp_sender_name = ""
#
smtp_server = "smtp.gmail.com"
smtp_port = 587
#
smtp_TLS = True


# Mail body / E-posta metni
mail_signature = ""
mail_title = ""
mail_contact = ""
# the curly brackets are mandatory / {} icindekiler zorunlu 
mail_body = ( 
    """
    <html>
    <head></head>
    <body>
    <p>Değerli Öğretim Üyemiz,</p>
    
    <p>Bölümümüzde vermekte olduğunuz <b>{name} ({_type} / {group} Grubu)</b> dersine 
    ait <b>"Ders Değerlendirme Anketi"</b> nin sonuçları ekte gönderilmiştir.
    Ders değerlendirme anket sonuçlarını göz önüne alarak yazacağınız
    <b>"Ders Değerlendirme Formu"</b> nu 7 gün içinde hazırlayarak MÜDEK arşivindeki
    ders klasörüne koymanız ve bir kopyasını Anabilim Dalı başkanınıza göndermeniz
    hususunda gereğini önemle rica ederim.</p>
    <br>
    <p>{signature}<br>
    {title}</p>
    <br>
    <br>
    <p><i>Not: Bu e-posta ve eki otomatik olarak oluşturulmuş ve gönderilmiştir.
    Bu e-postayı yanıtlamayınız. Eğer bir hata olduğunu düşünüyorsanız
    &lt;{contact}&gt; adresine durumu bildiriniz.</i></p>
    </body>
    </html>
    """)