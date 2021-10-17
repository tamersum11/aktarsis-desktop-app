import aktarsis_db_connector as adbc
from datetime import datetime 

id_log = "6"
id_reg = "7"
id_cp = "8"
id_cns = "9"
id_ct = "10"
id_cph = "11"
id_cdp = "12"
id_cds = "13"
id_cdl = "14"
id_logout = "15"

date = datetime.now().strftime("%Y-%m-%d")
time = datetime.now().strftime("%H:%M:%S")

def userLogin(mail_adres, sifre):
    global id_log, date, time
    user_info = adbc.whereOperation("*", "kullanicilar", "mail", mail_adres)

    if len(user_info) == 0:
        label_giris_hata = "Geçersiz Mail!!!"
        login_info = False
    else:
        if sifre != user_info[0][4]:
            label_giris_hata = "Hatalı şifre!!!"
            login_info = False
        else:
            add_user_log = (user_info[0][0], id_log, date, time)
            adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_log)
            label_giris_hata = f"Hoşgeldin {user_info[0][1]} {user_info[0][2]}..."
            login_info = True
    
    return label_giris_hata, login_info, user_info

def userLogout(id_user):
    global id_logout, date, time

    add_user_logout = [id_user, id_logout, date, time]
    adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_logout)
 
def userUpdatePassword(ad, soyad, mail_adres, sifre_1, sifre_2):
    global id_cp, date, time
    user_info = adbc.whereOperation("*", "kullanicilar", "mail", mail_adres)

    if len(user_info) == 0:
        label_sy_hata = "Geçersiz Mail!!!"
        update_password_info = False
    else:
        if ad != user_info[0][1]:
            label_sy_hata = "Geçersiz Ad!!!"
            update_password_info = False
        elif soyad != user_info[0][2]:
            label_sy_hata = "Geçersiz Soyad!!!"
            update_password_info = False
        elif ad == user_info[0][1] and soyad == user_info[0][2]:
            if len(sifre_1) > 4 or len(sifre_2) > 4:
                label_sy_hata = "Şifre 4 Karakter Olmalı!!!"
                update_password_info = False
            elif len(sifre_1) < 4 or len(sifre_2) < 4:
                label_sy_hata = "Şifre 4 Karakter Olmalı!!!"
                update_password_info = False
            elif len(sifre_1) == 4:
                if " " in sifre_1 or " " in sifre_2:
                    label_sy_hata = "Şifrede Boşluk Olmamalı!!!"
                    update_password_info = False
                else:
                    if sifre_1 == sifre_2:
                        add_user_cp = (user_info[0][0], id_cp, date, time)
                        adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_cp)
                        adbc.updateOperation("kullanicilar", "sifre", "id", sifre_1, user_info[0][0])
                        result = adbc.whereOperation("*", "kullanicilar", "mail", mail_adres)
                        label_sy_hata = f"Şifreniz Başarıyla Yenilendi! Yeni Şifreniz: {result[0][4]}"
                        update_password_info = True
                    else:
                        label_sy_hata = "Girilen Şifreler Aynı Değil!!!"
                        update_password_info = False
    
    return label_sy_hata, update_password_info

def userUpdateNameSurname(user_id, new_name, new_surname):
    global id_cns, date, time
    check_user = adbc.whereOperation("*", "kullanicilar", "id", user_id)

    if len(check_user) == 0:
        label_cns_err = "Geçersiz Kullanıcı ID!!!"
    elif len(new_name) == 0:
        label_cns_err = "Ad Boş Bırakılamaz!!!"
    elif len(new_surname) == 0:
        label_cns_err = "Soyad Boş Bırakılamaz!!!"
    elif len(new_name) > 45:
        label_cns_err = "Ad Uzunluğu En Fazla 45 Karakter Olmalı!!!"
    elif len(new_surname) > 45:
        label_cns_err = "Soyad Uzunluğu En Fazla 45 Karakter Olmalı!!!"
    elif " " in new_surname:
        label_cns_err = "Soyadında Boşluk Olmamalı!!!"
    else:
        adbc.updateOperation("kullanicilar", "ad", "id", new_name, user_id)
        adbc.updateOperation("kullanicilar", "soyad", "id", new_surname, user_id)

        add_cns = [user_id, id_cns, date, time]
        adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_cns)

        res_cns = adbc.whereOperation("*", "kullanicilar", "id", user_id)

        label_cns_err = f"Ad: {res_cns[0][1]}, Soyad: {res_cns[0][2]} Olarak Başarıyla Yenilendi"

    return label_cns_err 

def userRegisteration(name, surname, email, device_id, password_1, password_2):
    global id_reg, date, time
    check_user = adbc.whereOperation("*", "kullanicilar", "mail", email)
    check_device = adbc.whereOperation("*", "cihazlar", "idcihazlar", device_id)
    add_user = (name, surname, email, password_1)

    if len(check_user) != 0:
        label_kayit_hata = "Geçersiz Mail!!!"
        registeration_info = False
    elif len(check_device) != 0:
        label_kayit_hata = "Geçersiz Cihaz Numarası!!!"
        registeration_info = False
    elif len(name) == 0:
        label_kayit_hata = "Ad Boş Bırakılamaz!!!"
        registeration_info = False
    elif len(surname) == 0:
        label_kayit_hata = "Soyad Boş Bırakılamaz!!!"
        registeration_info = False
    elif len(email) == 0:
        label_kayit_hata = "Mail Boş Bırakılamaz!!!"
        registeration_info = False
    elif len(name) > 45:
        label_kayit_hata = "Ad Uzunluğu En Fazla 45 Karakter Olmalı!!!"
        registeration_info = False
    elif len(surname) > 45:
        label_kayit_hata = "Soyad Uzunluğu En Fazla 45 Karakter Olmalı!!!"
        registeration_info = False
    elif len(email) > 100:
        label_kayit_hata = "Mail Uzunluğu En Fazla 100 Karakter Olmalı!!!"
        registeration_info = False
    elif len(device_id) == 0:
        label_kayit_hata = "Cihaz Numarası Boş Bırakılamaz!!!"
        registeration_info = False
    elif " " in surname:
        label_kayit_hata = "Soyadında Boşluk Olmamalı!!!"
        registeration_info = False
    elif "mail.com" not in email or " " in email:
        label_kayit_hata = "Geçersiz Mail!!!"
        registeration_info = False
    elif len(password_1) > 4 or len(password_2) > 4:
        label_kayit_hata = "Şifre 4 Karakter Olmalı!!!"
        registeration_info = False
    elif len(password_1) < 4 or len(password_2) < 4:
        label_kayit_hata = "Şifre 4 Karakter Olmalı!!!"
        registeration_info = False
    elif len(password_1) == 4:
        if " " in password_1 or " " in password_2:
            label_kayit_hata = "Şifrede Boşluk Olmamalı!!!"
            registeration_info = False
        else:
            if password_1 == password_2:
                adbc.insertOperation("kullanicilar", "(ad, soyad, mail, sifre)", add_user)
                user_info = adbc.whereOperation("*", "kullanicilar", "mail", email)
                add_user_reg = (user_info[0][0], id_reg, date, time)
                adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_reg)
                label_kayit_hata = "Kayıt İşlemi Başarıyla Gerçekleşti!"
                registeration_info = True
            else:
                label_kayit_hata = "Girilen Şifreler Aynı Değil!!!"
                registeration_info = False
    
    return label_kayit_hata, registeration_info

def userDeviceInfo(user_info):
    user_device_info = adbc.whereOperation("*", "cihazlar", "idkullanicilar", user_info[0][0])

    return user_device_info

def setDCHTable(device_no):
    device_info = adbc.whereOperation("*", "cihazlar", "idcihazlar", device_no[10:])
    plant_info = adbc.whereOperation("*", "bitkiler", "id", device_info[0][2])
    soil_info = adbc.whereOperation("*", "topraklar", "id", device_info[0][3])
    location_info = device_info[0][4]

    return plant_info, soil_info, location_info   

def setChosenDevice(device_status):
    device_info = adbc.whereOperation("*", "cihazlar", "idcihazlar", device_status[10:])

    return device_info

def setChosenDateText(id_device, chosen_date):
    proccess_list = []
    device_proccess_info = adbc.whereOperation("*", "cihaz_islemler", "idcihazlar", id_device)

    for x in device_proccess_info:
        if x[3] == chosen_date:
            proccess_list.append(x)

    text_line_plant = []
    text_line_1_plant = f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">{chosen_date} Tarihli İşlemler:</span></p>\n"
    text_line_plant.append(text_line_1_plant)

    if len(proccess_list) == 0:
        text_line_2_plant = "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Bu tarihte bir işlem yapılmamıştır. </p></body></html>"
        text_line_plant.append(text_line_2_plant)
    else:
        for x in proccess_list:
            proccess = adbc.whereOperation("*", "islem_turleri", "idislem_turleri", x[2])
            text_line_2_plant = f"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">{x[4]} saatinde {proccess[0][1]} işlemi yapılmıştır. Hava Sıcaklığı {x[5]} Derece, Hava Nemi %{x[6]}, Toprak Nemi %{x[7]}, Ph Değeri {x[8]} olarak ölçülmüştür. </p>\n"
            text_line_plant.append(text_line_2_plant)
        
        text_line_last_plant = "</body></html>"
        text_line_plant.append(text_line_last_plant)
    
    return text_line_plant

def setProccessList(id_device):
    proccess_list = []
    device_proccess_info = adbc.whereOperation("*", "cihaz_islemler", "idcihazlar", id_device)

    for x in device_proccess_info:
        proccess = adbc.whereOperation("*", "islem_turleri", "idislem_turleri", x[2])
        list_item = f"Tarih: {x[3]} Saat: {x[4]} İşlem: {proccess[0][1]} Sıcaklık(Hava): {x[5]} Nem(Hava): {x[6]} Nem(Toprak): {x[7]} PH: {x[8]}"
        proccess_list.append(list_item)
    
    return proccess_list

def setSpinBoxSetPlant(id_plant):
    plant_info = adbc.whereOperation("*", "bitkiler", "id", id_plant)

    ph_min = plant_info[0][10]
    ph_max = plant_info[0][11]

    return ph_min, ph_max

def updateTimeEditSetPlant(id_user, id_device, update_time):
    global id_ct, date, time

    adbc.updateOperation("cihazlar", "atananzaman", "idcihazlar", update_time, id_device)
    result = adbc.whereOperation("*", "cihazlar", "idcihazlar", id_device)

    add_update_time = [id_user, id_ct, date, time]
    adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_update_time)

    return result

def updatePHEditSetPlant(id_user, id_device, update_ph):
    global id_cph, date, time

    adbc.updateOperation("cihazlar", "atananph", "idcihazlar", update_ph, id_device)
    result = adbc.whereOperation("*", "cihazlar", "idcihazlar", id_device)

    add_update_ph = [id_user, id_cph, date, time]
    adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_update_ph)

    return result

def setPanel(id_device):
    global date
    
    panel_proccess_list = []
    device_panel_list = adbc.whereOperation("*", "panel", "idcihaz", id_device)

    for x in device_panel_list:
        if x[2] == date:
            panel_info = True
            generated_energy = x[3]
            consumed_energy = x[4]
        else:
            panel_info = False
            generated_energy = "Bu tarihe dair kayıt yok!"
            consumed_energy = "Bu tarihe dair kayıt yok!"
        
        panel_list_item = f"{x[2]} tarihinde Üretilen Enerji: {x[3]}Wh  Tüketilen Enerji: {x[4]}Wh"
        panel_proccess_list.append(panel_list_item)
    
    return panel_proccess_list, panel_info, generated_energy, consumed_energy

def setSetDeviceTable(device_id):
    device = adbc.whereOperation("*", "cihazlar", "idcihazlar", device_id)
    plant_info = adbc.whereOperation("*", "bitkiler", "id", device[0][2])
    soil_info = adbc.whereOperation("*", "topraklar", "id", device[0][3])
    location_info = device[0][4]

    return plant_info, soil_info, location_info   

def updateChangesSetDevice(device, change_plant_info, change_soil_info, change_location_info):
    global id_cph, id_cdp, id_cds, id_cdl, date, time

    if change_plant_info[0] and change_soil_info[0] and change_location_info[0]:
        adbc.updateOperation("cihazlar", "idbitkiler", "idcihazlar", change_plant_info[1], device[0][0])
        adbc.updateOperation("cihazlar", "idtopraklar", "idcihazlar", change_soil_info[1], device[0][0])
        adbc.updateOperation("cihazlar", "cihazkonum", "idcihazlar", change_location_info[1], device[0][0])
        max_ph = adbc.whereOperation("*", "bitkiler", "id", change_plant_info[1])
        adbc.updateOperation("cihazlar", "atananph", "idcihazlar", max_ph[0][11], device[0][1])
        
        add_user_cdp = [device[0][1], id_cdp, date, time]
        adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_cdp)
        add_user_cds = [device[0][1], id_cds, date, time]
        adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_cds)
        add_user_cdl = [device[0][1], id_cdl, date, time]
        adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_cdl)
        add_user_cph = [device[0][1], id_cph, date, time]
        adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_cph)

        label_change_info = "Cihazda Bitki, Toprak ve Konum Değişti!"
    
    elif not change_plant_info[0] and change_soil_info[0] and change_location_info[0]:
        adbc.updateOperation("cihazlar", "idtopraklar", "idcihazlar", change_soil_info[1], device[0][0])
        adbc.updateOperation("cihazlar", "cihazkonum", "idcihazlar", change_location_info[1], device[0][0])

        add_user_cds = [device[0][1], id_cds, date, time]
        adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_cds)
        add_user_cdl = [device[0][1], id_cdl, date, time]
        adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_cdl)

        label_change_info = "Cihazda Toprak  ve Konum Değişti!"

    elif change_plant_info[0] and not change_soil_info[0] and change_location_info[0]:
        adbc.updateOperation("cihazlar", "idbitkiler", "idcihazlar", change_plant_info[1], device[0][0])
        adbc.updateOperation("cihazlar", "cihazkonum", "idcihazlar", change_location_info[1], device[0][0])
        max_ph = adbc.whereOperation("*", "bitkiler", "id", change_plant_info[1])
        adbc.updateOperation("cihazlar", "atananph", "idcihazlar", max_ph[0][11], device[0][1])
        
        add_user_cdp = [device[0][1], id_cdp, date, time]
        adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_cdp)       
        add_user_cdl = [device[0][1], id_cdl, date, time]
        adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_cdl)
        add_user_cph = [device[0][1], id_cph, date, time]
        adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_cph)
        
        label_change_info = "Cihazda Bitki ve Konum Değişti!"
    
    elif change_plant_info[0] and change_soil_info[0] and not change_location_info[0]:
        adbc.updateOperation("cihazlar", "idbitkiler", "idcihazlar", change_plant_info[1], device[0][0])
        adbc.updateOperation("cihazlar", "idtopraklar", "idcihazlar", change_soil_info[1], device[0][0])
        max_ph = adbc.whereOperation("*", "bitkiler", "id", change_plant_info[1])
        adbc.updateOperation("cihazlar", "atananph", "idcihazlar", max_ph[0][11], device[0][1])
        
        add_user_cdp = [device[0][1], id_cdp, date, time]
        adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_cdp)
        add_user_cds = [device[0][1], id_cds, date, time]
        adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_cds) 
        add_user_cph = [device[0][1], id_cph, date, time]
        adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_cph)

        label_change_info = "Cihazda Bitki ve Toprak Değişti!"
    
    elif change_plant_info[0] and not change_soil_info[0] and not change_location_info[0]:
        adbc.updateOperation("cihazlar", "idbitkiler", "idcihazlar", change_plant_info[1], device[0][0])
        max_ph = adbc.whereOperation("*", "bitkiler", "id", change_plant_info[1])
        adbc.updateOperation("cihazlar", "atananph", "idcihazlar", max_ph[0][11], device[0][1])
        
        add_user_cdp = [device[0][1], id_cdp, date, time]
        adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_cdp)
        add_user_cph = [device[0][1], id_cph, date, time]
        adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_cph)       
        
        label_change_info = "Cihazda Bitki Değişti!"
    
    elif not change_plant_info[0] and change_soil_info[0] and not change_location_info[0]:
        adbc.updateOperation("cihazlar", "idtopraklar", "idcihazlar", change_soil_info[1], device[0][0])
        
        add_user_cds = [device[0][1], id_cds, date, time]
        adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_cds) 
        
        label_change_info = "Cihazda Toprak Değişti!"
    
    elif not change_plant_info[0] and not change_soil_info[0] and change_location_info[0]:
        adbc.updateOperation("cihazlar", "cihazkonum", "idcihazlar", change_location_info[1], device[0][0])

        add_user_cdl = [device[0][1], id_cdl, date, time]
        adbc.insertOperation("kullanici_islemler", "(idkullanicilar, idislemturu, tarih, saat)", add_user_cdl)

        label_change_info = "Cihazda KonumDeğişti!"
    
    elif not change_plant_info[0] and not change_soil_info[0] and not change_location_info[0]:
        label_change_info = "Cihazda Değişiklik Olmadı!"
    
    return label_change_info

def setListUserProccessEditUser(user_id):
    list_proccess_eu = []
    user_proccess = adbc.whereOperation("*", "kullanici_islemler", "idkullanicilar", user_id)

    for x in user_proccess:
        proccess = adbc.whereOperation("*", "islem_turleri", "idislem_turleri", x[2])
        list_item_eu = f"{x[3]} {x[4]} Tarihinde {proccess[0][1]} İşlemi Gerçekleşmiştir"

        list_proccess_eu.append(list_item_eu)
    
    return list_proccess_eu

def calculatePlantingDate(device_id, plant_id):

    feeding_counter = 0
    lightning_counter = 0

    nonideal_temp_counter = 0
    nonideal_hum_counter = 0
    nonideal_moisture_counter = 0
    nonideal_ph_counter = 0

    list_device_proccess = adbc.whereOperation("*", "cihaz_islemler", "idcihazlar", device_id)
    list_plant_info = adbc.whereOperation("*", "bitkiler", "id", plant_id)

    default_planting_date = list_plant_info[0][14]
    feeding_constant = list_plant_info[0][14] / list_plant_info[0][13] 
    constant_for_plant = list_plant_info[0][14] / feeding_constant   

    if len(list_device_proccess) == 0:
        text_info = f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Cihazın İşlem Kaydı Bulunmamaktadır!!! Cihazınızda ekili olarak kayıtlı bulunan {list_plant_info[0][1]} için yeni ekildiği varsayılmıştır. Tahmini ekin verme süresi {default_planting_date} gündür. </span></p>\n"

        return text_info
    
    elif len(list_device_proccess) > 0:

        for x in list_device_proccess:
            if x[2] == 1:
                feeding_counter += 1
            elif x[2] == 4:
                lightning_counter += 1
            elif x[5] < list_plant_info[0][6] or x[5] > list_plant_info[0][7]:
                nonideal_temp_counter += 1
            elif x[6] < list_plant_info[0][8] or x[6] > list_plant_info[0][9]:
                nonideal_hum_counter += 1
            elif x[7] < list_plant_info[0][8] or x[7] > list_plant_info[0][9]:
                nonideal_moisture_counter += 1
            elif x[8] < list_plant_info[0][10] or x[8] > list_plant_info[0][11]:
                nonideal_ph_counter += 1
        
        planting_date = default_planting_date - (constant_for_plant * (feeding_constant - (feeding_counter % feeding_constant))) + (nonideal_temp_counter * 2) + (nonideal_hum_counter * 2) + (nonideal_moisture_counter * 3) + (nonideal_ph_counter * 4)

        if planting_date <= 0 or feeding_counter > 2 * feeding_constant:
            text_info = f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Cihazınızda ekili olarak kayıtlı bulunan {list_plant_info[0][1]} tahminen ekin vermiştir... </span></p>\n"
        elif planting_date > 0:
            text_info = f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Cihazınızda ekili olarak kayıtlı bulunan {list_plant_info[0][1]} için tahmini ekin verme süresi {int(planting_date)} gündür... </span></p>\n"

        return text_info


