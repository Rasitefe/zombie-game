# Zombie Game - Git ve Python Ortam Kurulumu
iklim çelebi 
Bu proje **Python 3.11** sürümü ile çalışmaktadır. Çalıştırmadan önce gerekli bağımlılıkları yükleyerek ortamı hazırlamanız gerekmektedir.

---

## **🛠 Git Kurulumu ve SSH Bağlantısı**

Öncelikle projeyi GitHub’dan çekebilmek için **Git’i bilgisayarınıza yükleyip hesabınıza bağlamanız gerekmektedir**.

### ** Git Yükleme ve Kontrol Etme (Windows)**
Eğer Git yüklü değilse, **[Git Resmi Sitesi](https://git-scm.com/)** üzerinden indirip yükleyin.

Yükledikten sonra **terminali (PowerShell veya Git Bash) yönetici olarak açın** ve şu komutu çalıştırarak Git’in kurulu olup olmadığını kontrol edin:

```
git --version
```

**Eğer aşağıdaki gibi bir çıktı alıyorsanız, Git başarıyla yüklüdür:**
```
git version 2.**.*.windows.*
```
**git'e kendi hesabını tanımlamak için şu kodları çalışıtırın**
```
git config --global user.name "git kullanıcı adın"
git config --global user.email "git email adresin@gmail.com"
git config --global --list
```
---

### ** SSH Anahtarı Oluşturma**
SSH anahtarı oluşturarak GitHub ile parolasız bağlantı kurabilirsiniz.

**SSH anahtarını oluşturmak için şu komutu çalıştırın:**
```
ssh-keygen -t rsa -b 4096 -C "senin_email_adresin@gmail.com"
```

Komut çalıştırıldığında **anahtarın kaydedileceği konum sorulacaktır**, **ENTER** tuşuna basarak varsayılan konumu kabul edin.

Ardından şu şekilde bir mesaj alacaksınız:
```
Enter passphrase (empty for no passphrase): [ENTER]
Enter same passphrase again: [ENTER]
```
**Burada boş bırakıp ENTER** tuşuna basarak her `git pull` işleminde parola girme zorunluluğunu kaldırabilirsiniz.

SSH anahtarı başarıyla oluşturulduğunda şu mesajı göreceksiniz:
```
Your identification has been saved in C:\Users\KULLANICI_ADI/.ssh/id_rsa
Your public key has been saved in C:\Users\KULLANICI_ADI/.ssh/id_rsa.pub
```

---

### ** SSH Anahtarını GitHub’a Ekleme**
**SSH bağlantısını GitHub ile kullanabilmek için public key’i eklemeniz gerekmektedir.**

1. **Public key’i almak için terminalde şu komutu çalıştırın:**
   ```
   Get-Content ~/.ssh/id_rsa.pub
   ```
2. **Çıkan uzun anahtarı tamamen kopyalayın**.
3. **GitHub’a giriş yapın settings kısmından** ve şu sayfaya gidin:  
    **[SSH and GPG Keys](https://github.com/settings/keys)**
4. **"New SSH Key" butonuna tıklayın.**
5. **Title olarak `"Zombie-Game"` yazabilirsiniz.**
6. **Key Type kısmında "Authentication Key" seçili kalsın.**
7. **Kopyaladığınız SSH anahtarını "Key" alanına yapıştırın.**
8. **"Add SSH Key" (Yeşil buton) tıklayarak ekleyin.**

---

### ** SSH Bağlantısını Test Etme**
SSH anahtarınızın doğru çalıştığını test etmek için **terminali yönetici olarak açın** ve şu komutu çalıştırın:

```
ssh -T git@github.com
```

Eğer bağlantı başarılıysa şu mesajı göreceksiniz:
```
Hi <GitHub Kullanıcı Adınız>! You've successfully authenticated, but GitHub does not provide shell access.
```
Bu mesajı aldıysanız, artık **GitHub ile SSH bağlantısı kuruldu!** 

---

### ** Git Kullanıcı Adı ve E-posta Tanımlama**
Aşağıdaki komutlarla GitHub hesabınızı bağlayın(tekrar yapıyorum garanti olması için):

```
git config --global user.name "git kullanıcı adın"
git config --global user.email "git email adresin@gmail.com"
git config --global --list
```

Bu ayarlar, commit'lerinizde isminiz ve e-posta adresinizin görünmesini sağlar.

Ayarların doğru yapıldığını doğrulamak için:
```
git config --global --list
```

---

### ** Projeyi Bilgisayarınıza Çekme (Git Clone)**
SSH bağlantınız başarılı olduğunda, **projeyi bilgisayarınıza indirebilirsiniz**.

Öncelikle **terminalde projeyi yüklemek istediğiniz dizine gidin**:
```
cd C:\Users\KULLANICI_ADI\Desktop
```

Şimdi, projeyi klonlayın:
```
git clone git@github.com:Rasitefe/zombie-game.git
```

Artık proje bilgisayarınıza inmiş olacak! 

---

## **🛠 Python Ortam Kurulumu**
Bu proje **Python 3.11** ile çalışmaktadır. **Bağımlılıkları yükleyerek ortamı hazırlayın**.

Projeye girin:
```
cd zombie-game
```

Sanal ortamı oluşturun ve aktifleştirin:

**Linux & macOS:**
```
python3.11 -m venv .venv
source .venv/bin/activate
```
**Windows (PowerShell):**
```
python -m venv .venv
.venv\Scripts\activate
```

Bağımlılıkları yükleyin:
```
pip install -r requirements.txt
```

---

## **🎮 Oyunu Çalıştırma**
Oyunu başlatmak için aşağıdaki komutları kullanın:

**Linux & macOS:**
```
python map_try.py
python main.py
```
**Windows (PowerShell):**
```
python map_try.py
python main.py
```

---

## ** Özet**
1. **Git’i yükleyin ve doğrulayın (`git --version`).**
2. **SSH anahtarını oluşturun ve GitHub’a ekleyin.**
3. **SSH bağlantısını test edin (`ssh -T git@github.com`).**
4. **Git kullanıcı adınızı ve e-postanızı tanımlayın (`git config --global user.name/email`).**
5. **Projeyi `git clone` ile bilgisayarınıza çekin.**
6. **Python ortamını kurun (`venv` oluşturup `pip install -r requirements.txt`).**
7. **Oyunu çalıştırın (`python map_try.py && python main.py`).**

**Artık `Zombie-Game` projesini kurup çalıştırabilirsiniz!** 
