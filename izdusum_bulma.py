# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Küp 1'e ait 10 adet köşe ve kesik nokta listesi 
# Her nokta (x, y, z, w) formatında Homojen Koordinat Sistemi kullanılarak tanımlanmıştır. w=1
kup1_noktalari=[
    # Orijinal birim küpün 8 köşesi:
    [0.0,0.0,0.0,1.0],  # Index 0 - (0,0,0) Kesilecek Köşe
    [1.0,0.0,0.0,1.0],  # Index 1
    [0.0,1.0,0.0,1.0],  # Index 2
    [1.0,1.0,0.0,1.0],  # Index 3
    [0.0,0.0,1.0,1.0],  # Index 4
    [1.0,0.0,1.0,1.0],  # Index 5
    [0.0,1.0,1.0,1.0],  # Index 6
    [1.0,1.0,1.0,1.0],  # Index 7
    
    # Kesik noktalar (kenar orta noktaları):
    [0.5,0.0,0.0,1.0],  # Index 8 - X ekseni üzerinde
    [0.0,0.5,0.0,1.0],  # Index 9 - Y ekseni üzerinde
    [0.0,0.0,0.5,1.0]   # Index 10 - Z ekseni üzerinde
]

# Matris İşlemleri
def matris_carpimi(matris_a,matris_b):
   # İki matrisi çarpar: Matris A (Nokta Matrisi) x Matris B (Dönüşüm Matrisi).
    satir_a = len(matris_a)
    if satir_a > 0:
         sutun_a = len(matris_a[0]) 
    else: 
         0
    satir_b = len(matris_b)
    if satir_b > 0:
        sutun_b = len(matris_b[0])  
    else: 
        0

    # A'nın sütunu B'nin satırına eşit olmalıdır (N=N).
    if sutun_a != satir_b:
        raise ValueError("Matrisler carpilmak icin uygun formatta degil.") 

    sonuc = [[0 for _ in range(sutun_b)] for _ in range(satir_a)]
    
    # matris çarpım algortiması bu sayede verilen iki matrisi uygun koşulları sağladığında iç içe döngüler kullanarak çarparız.
    for i in range(satir_a): 
        for j in range(sutun_b):
            toplam = 0
            for k in range(sutun_a):
                toplam += matris_a[i][k] * matris_b[k][j]
            sonuc[i][j] = toplam 
            
    return sonuc

# izometrik izdüşüm matrisi
# x ekseni etrafında 45 derece, z ekseni etrafında 30 derece döndürme işlemleri
cos30 = 0.866025
sin30 = 0.5
cos45 = 0.707106
sin45 = 0.707106 

izdusum_matrisi = [
    [cos30,sin30 * cos45,sin30 * sin45,0.0],
    [-sin30,cos30 * cos45,cos30 * sin45,0.0],
    [0.0,-sin45,cos45,0.0],
    [0.0,0.0,0.0,1.0]    
]

# öteleme işlemleri
def oteleme_matrisi(tx, ty, tz):
    #Homojen koordinatlarda öteleme matrisini döndürür.
    return [
        [1.0,0.0,0.0,0.0],
        [0.0,1.0,0.0,0.0],
        [0.0,0.0,1.0,0.0],
        [tx,ty,tz,1.0]
    ]

# Küp 2'yi X ekseni boyunca 1 birim ötele
oteleX = oteleme_matrisi(1.0,0.0,0.0)
# Küp 3'ü Y ekseni boyunca 1 birim ötele
oteleY = oteleme_matrisi(0.0,1.0,0.0)
# Küp 4'ü Z ekseni boyunca 1 birim ötele
oteleZ = oteleme_matrisi(0.0,0.0,1.0)


# Çizim ayarlama işleri
def cizim_ayarlama():
   
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    # Görseli ekran merkezine taşıma ve büyütme
    glTranslate(0, 0, -5)  # Kamerayı geriye çek
    glScale(1.0, 1.0, 1.0)  # Ölçeği normale çevir

def koordinat_cizim():
    
    eksen_noktalari = [
        [0.0,0.0,0.0,1.0], # Merkez (0,0,0)
        [2.0,0.0,0.0,1.0], # x ekseni ucu 
        [0.0,2.0,0.0,1.0], # y ekseni ucu 
        [0.0,0.0,2.0,1.0]  # z ekseni ucu 
    ]

    # Eksen noktalarına izometrik dönüşümü uygular.
    izdusum_eksen = matris_carpimi(eksen_noktalari, izdusum_matrisi)

    glBegin(GL_LINES) # Çizgi çizim modunu başlatır.
    
    # X ekseni (Kırmızı)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(izdusum_eksen[0][0],izdusum_eksen[0][1],izdusum_eksen[0][2])
    glVertex3f(izdusum_eksen[1][0],izdusum_eksen[1][1],izdusum_eksen[1][2])

    # Y ekseni (Yeşil)
    glColor3f(0.0, 1.0, 0.0) 
    glVertex3f(izdusum_eksen[0][0],izdusum_eksen[0][1],izdusum_eksen[0][2])
    glVertex3f(izdusum_eksen[2][0],izdusum_eksen[2][1],izdusum_eksen[2][2])

    # Z ekseni (Mavi)
    glColor3f(0.0, 0.0, 1.0) 
    glVertex3f(izdusum_eksen[0][0],izdusum_eksen[0][1],izdusum_eksen[0][2])
    glVertex3f(izdusum_eksen[3][0],izdusum_eksen[3][1],izdusum_eksen[3][2])

    glEnd()

def kup_kenar_cizme(nokta_list):
    # (0,0,0) köşesi kesilmiş, üç kenar orta noktasına bağlanmış
    kesik_kup_kenarlari = [
        # Alt yüz (z=0):
        (1,3), (3,2), (2,1),
        
        # Üst yüz (z=1):
        (4,5), (5,7), (7,6), (6,4), 
        
        # Dikey kenarlar:
        (1,5), (2,6), (3,7),
        
        # Kesik köşe kenarları
        (1,8),  
        (2,9),  
        (4,10),
        
        # kesilen yüzey:
        (8,9), (9,10), (10,8)
    ]

    glBegin(GL_LINES)

    for idx1, idx2 in kesik_kup_kenarlari:
        glVertex3f(nokta_list[idx1][0], nokta_list[idx1][1], nokta_list[idx1][2])
        glVertex3f(nokta_list[idx2][0], nokta_list[idx2][1], nokta_list[idx2][2])
    glEnd()

# Ana Çizim Aşaması
def son_cizim_asamasi():
    # Yazdığımız değişkenleri bu fonksiyon üzerinde işlem yapmak için global kullanarak tanımlarız.
    global kup1_noktalari, izdusum_matrisi, oteleX, oteleY, oteleZ 
    
    # Küp 1'in izdüşümü (Orijinal Küp)
    izdusum_kup1 = matris_carpimi(kup1_noktalari, izdusum_matrisi)
    
    # Küp 2'nin izdüşümü (X öteleme) 
    # İzDüşüm matrisiyle öteleme matrisinin çarpımıyla elde edilen toplam dönüşüm matrisi
    T_kup2_izdusum = matris_carpimi(oteleX, izdusum_matrisi)
    izdusum_kup2 = matris_carpimi(kup1_noktalari, T_kup2_izdusum)

    # Küp 3'ün izdüşümü (Y öteleme)
    T_kup_3_izdusum = matris_carpimi(oteleY, izdusum_matrisi)
    izdusum_kup3 = matris_carpimi(kup1_noktalari, T_kup_3_izdusum)

    # Küp 4'ün izdüşümü (Z öteleme)
    T_kup_4_izdusum = matris_carpimi(oteleZ, izdusum_matrisi)
    izdusum_kup4 = matris_carpimi(kup1_noktalari, T_kup_4_izdusum)

    cizim_ayarlama()

    koordinat_cizim() # Eksenleri çizme

    # Küpleri beyaz renkte çizme
    glColor3f(1.0,1.0,1.0) 
   
    # Dört küpün de kenar çizimini gerçekleştirir.
    kup_kenar_cizme(izdusum_kup1)
    kup_kenar_cizme(izdusum_kup2)
    kup_kenar_cizme(izdusum_kup3)
    kup_kenar_cizme(izdusum_kup4)

    #Çizimi ekrana yansıtmak için kullanılır.
    pygame.display.flip()

# Ana Döngü ve Pygame'i başlatma
def main():

    pygame.init() # Pygame'i başlatır.
    glutInit()  # PyOpenGL (GLUT) kütüphanesini başlatır.
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
   
    pygame.display.set_caption("Kupun Izometrik Iz Dusumu | BG_KisaSinav_2") 

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    #2D/3D düzlemde projeksiyon ayarı yapılır.
    gluPerspective(45, 800/600, 0.1, 50.0)  # Perspektif projeksiyon

    glMatrixMode(GL_MODELVIEW)
    
    # Arka plan rengini siyah yapma
    glClearColor(0.0, 0.0, 0.0, 1.0)

    dongu = True
    
    while dongu:
        # Klavye/Fare girdilerini ve kapatma isteğini işler.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                dongu = False
                
        son_cizim_asamasi() # Ana çizim fonksiyonunu çağırır.
        pygame.time.wait(10) # 10 milisaniye bekler (Döngü hızını kontrol eder).
        
    pygame.quit() # Programdan çıkar.

if __name__ == '__main__':
    main()