# Makan Bang

### Tautan deployment aplikasi: http://fariz-muhammad31-makanbang.pbp.cs.ui.ac.id/


## Nama-nama anggota kelompok:
- Fariz Muhammad Rayhansyah Ramadhan - 2306203854
- Irma Nia Alwijah - 2306226864
- Maibyna Khairanisya - 2306165723
- Meutia Fajriyah - 2306165635
- Muhammad Ghathaf Fariz Abiyyu - 2306210203
- Jeremi Felix Adiyatma - 2306219575

## Deskripsi aplikasi 
Travelling ke wilayah baru, rasanya kurang lengkap jika tidak berbicara tentang jajan dan makan-makan. Bukan soal mencari makanan khas kearifan lokalnya, tapi perihal memilih banyak opsi dan mencicipi masakan yang ada. Terlebih di kota besar seperti Jakarta, dengan jutaan warung makan dan restoran yang menjamur, bersama rekomendasi populer yang terlalu sering ditawarkan. Rasanya, porsi hari ini pun menjadi perihal yang berat untuk diputuskan.

Terinspirasi dari problematika tersebut, “Makan Bang” tertarik untuk mengembangkan platform digital untuk membantu traveler dan sobat makan-makan mencari sajian terbaik, memastikan anda mampu memilih menu hari ini! Dengan mengelola informasi di seputar Jakarta Selatan, “Makan Bang” juga menyiapkan tautan menuju platform Gofood by Gojek, agar menu yang diinginkan siap antar. 

“Makan Bang” dilengkapi dengan informasi mengenai gizi dalam menu-menu yang disajikan, membuat sobat “Makan Bang” bisa mengira-ngira, nutrisi yang akan disantap hari ini. Dalam penggunaannya pun, sobat tidak perlu khawatir, “Makan Bang” sudah menambahkan fitur preference serta catalog list yang membantu menyortir makanan favorit, serta mengubahnya kembali di lain waktu. “Makan Bang” juga memiliki meal-planning untuk rencana mukbang sobat makan-makan selanjutnya, lho! 

Eits, jangan takut menu yang tadinya menggiurkan banget, nggak bisa ditemukan lagi, karena “Makan Bang” punya bookmark yang membantu menyimpan list menu simpananmu. Jika setelah icip-icip, terdapat kekurangan, sobat juga bisa mencurahkan rate and review-nya, ya! SIlakan bertanya juga di kolom Forum, yang akan membantu sesama sobat “Makan Bang” untuk berbagi keseruan kulinerannya. Seru kan?

Selain membantu traveler, “Makan Bang” juga bermanfaat bagi para pengusaha makanan, terutama di Jakarta Selatan. Lewat fitur review dan rating dari pengguna, restoran dan pedagang kaki lima jadi lebih dikenal dan mudah dijangkau. Warga lokal pun bisa lebih mudah menemukan tempat makan baru, membuat wishlist, dan menandai tempat-tempat yang sudah mereka kunjungi.

## Daftar Modul yang Akan Diimplementasikan
### Rate and Review 🌟<br>
Pada modul ini, pengguna dapat memberikan penilaian berbentuk bintang (1-5) serta menulis ulasan dalam teks mengenai makanan yang sesuai. Fitur ini membantu pengguna lain dalam mendapatkan gambaran mengenai cita rasa dari makanan yang ada pada katalog.<br>

### Meal Planning 📑
Pada modul ini, pengguna dapat memilih makanan atau minuman dan menambahkannya ke jadwal yang sudah mereka buat. Modul ini memberikan kebebasan bagi pengguna untuk melakukan penambahan, penghapusan, atau perubahan menu pada jadwalnya.

### Preference 💗
Modul ini memungkinkan pengguna untuk memilih preferensi makanan apa yang mereka inginkan. Dengan modul ini, pengguna akan mendapatkan rekomendasi yang lebih personal dan relevan sesuai dengan preferensi mereka.

### Catalog List 🍱
Modul ini melakukan penyaringan product saat pengguna ingin melakukan pencarian berdasarkan kategori atau harga yang sesuai. Jika pengguna adalah admin, terdapat button tambahan pada halaman ini untuk melakukan penambahan product yang nantinya akan ditampilkan pada katalog.

### Forum 📜
Pada modul ini, pengguna yang sudah memiliki akun dapat membuat forum atau ikut menjawab forum yang sudah ada sebelumnya. Pengguna dapat bertanya mengenai rekomendasi, saran, ataupun berbagi pengalamannya dengan bebas pada forum ini.

### Bookmark 🔖
Modul ini memberikan rangkuman dari makanan atau minuman yang sudah disimpan oleh pengguna. Pengguna dapat menandakan makanan atau minuman yang ada pada list ini jika sudah mencobanya.

## Sumber Initial Dataset 
https://docs.google.com/spreadsheets/d/10_JHj928fFrLtnYP9vN8PU7qrf5Y_hXX7gnLIM1BHUw/edit?usp=sharing <br>

Kami memperoleh dataset dari Gofood by Gojek menggunakan metode scraping.

## Role atau peran pengguna beserta deskripsinya 

### Logged In User:

### Admin
- <b>Add Product: </b> Menambahkan produk makanan baru ke dalam katalog.

- <b>Edit Product: </b>Memperbarui informasi produk yang sudah ada.

- <b>Delete Product: </b>Menghapus produk yang sudah tidak tersedia atau tidak relevan.

- <b>Manage Reviews: </b>menghapus, atau mengedit ulasan yang tidak sesuai.

- <b>Manage Forum: </b>Mengawasi dan mengelola konten forum

___
### User

- <b>Profile Management: </b>Mengedit profil pribadi, termasuk informasi kontak dan preferensi makanan.

- <b>Edit Preferences: </b>Mengubah preferensi makanan untuk personalisasi konten yang ditampilkan.

- <b>View Products: </b>Menelusuri dan melihat detail produk makanan.

- <b>Filter Products: </b>Menyaring produk berdasarkan kategori, harga, lokasi, dll.

- <b>Save to Bookmark: </b>Menandai produk sebagai favorit yang sudah dicoba atau ingin dicoba.

- <b>Manage Bookmarks: </b>Menambah atau menghapus produk dari bookmark.

- <b>Write Reviews: </b>Memberikan penilaian dan ulasan terhadap produk yang telah dicoba.

- <b>View Reviews: </b>Membaca ulasan yang ditulis oleh pengguna lain.

- <b>Rate and Review: </b>Memberikan rating bintang dan ulasan teks pada produk.

- <b>Participate in Forum: </b>Berpartisipasi dalam diskusi di forum, mengajukan pertanyaan, atau memberikan jawaban.

- <b>Meal Planning: </b>Membuat dan mengelola rencana makanan berdasarkan preferensi.

- <b>Receive Recommendations: </b>Mendapatkan rekomendasi produk berdasarkan aktivitas dan preferensi.

___

### Tidak Login

### Guest:

- <b>View Products: </b>Menelusuri dan melihat daftar produk makanan yang tersedia.

- <b>View Reviews: </b>Membaca ulasan yang telah ditulis oleh pengguna terdaftar.




