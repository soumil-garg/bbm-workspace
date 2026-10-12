"""Copy the 16 round 2 creatives into the approval folder with clean names and rebuild the three numbered sheets.
  python deliver_round2.py"""
import os, shutil, subprocess
D = 'C:/Users/soumi/OneDrive/Desktop/Daigo Ads/Round 2/For Approval'
os.makedirs(D, exist_ok=True)
KEY = [
    (1, 'R2_L_Hostel', '01_Hostel_mein_dahi_Mazaak_mat_karo', 'poster: hostel (lettering in the picture)'),
    (2, 'R2_L_Train', '02_Ticket_confirm_Chaas_confirm', 'poster: train (lettering in the picture)'),
    (3, 'R2_L_Roof', '03_Ghar_door_Chaas_paas', 'poster: terrace at dusk (lettering in the picture)'),
    (4, 'R2_L_Office', '04_Meeting_khatam_Chaas_break', 'poster: office pantry (lettering in the picture)'),
    (5, 'R2_L_Road', '05_Road_trip_Chaas_pack_hai', 'poster: road trip (lettering in the picture)'),
    (6, 'R2_L_Note', '06_Room_204_ki_chaas', 'native: tape note on a steel glass'),
    (7, 'R2_T_Hostel', '07_Mess_ka_khana_Apni_chaas', 'typed headline on a navy band: hostel'),
    (8, 'R2_T_Train', '08_Sleeper_mein_bhi_chaas', 'typed headline on a green band: train'),
    (9, 'R2_T_PG', '09_PG_mein_mixer_kaun_dhoyega', 'typed headline on a yellow band: PG kitchen'),
    (10, 'R2_T_Steps', '10_Phaado_Daalo_Hilao_Chaas', 'typed headline on a blue photo: three steps'),
    (11, 'R2_T_Roof', '11_Ghar_se_door_Chaas_se_nahi', 'typed headline on the dusk photo'),
    (12, 'R2_T_Roommates', '12_Sachet_kam_padenge_20_ka_pack', 'offer: 20-pack, 5% off prepaid'),
    (13, 'R2_T_Bag', '13_Bag_mein_chaas_ki_dukaan', 'graphic: bag and price strip'),
    (14, 'R2_T_Price', '14_Rs_28_ka_glass', 'graphic: price per glass'),
    (15, 'R2_T_Bold', '15_Dahi_jamana_nahi_Mixer_dhona_nahi', 'graphic: bold type on yellow'),
    (16, 'R2_T_Chat', '16_Mummy_chat', 'native: chat with Mummy'),
]
for n, i, name, label in KEY:
    shutil.copy('C:/cca/daigo/round2/img/%s.png' % i, '%s/%s.png' % (D, name))


def sheet(title, nums, cols):
    args = ['%d:%s:%s' % (n, i, label) for n, i, name, label in KEY if n in nums]
    out = '%s/Sheet %s.jpg' % (D, title)
    subprocess.run(['python', 'C:/cca/daigo/round2/sheet_round2.py', out, '620', str(cols)] + args, check=True)


sheet('1 - posters with the lettering in the picture, numbers 1 to 6', range(1, 7), 3)
sheet('2 - typed headlines, numbers 7 to 12', range(7, 13), 3)
sheet('3 - graphic and native, numbers 13 to 16', range(13, 17), 2)
print('delivered', len(KEY), 'creatives to', D)
