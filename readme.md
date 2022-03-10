## Product Service

### Spesifikasi :

* Bahasa Pemrograman : Python 3.9
* Framework : Flask + SqlAlchemy (ORM)
* Database : Postgresql
* Cache : Redis
* Container : Docker & docker-compose (development) 

----

Terdapat 1 endpoint `/product` dengan method `GET` yang digunakan untuk pengambil data dan `POST` untuk menambah data.

Terdapat fungsi redis untuk melakukan cache data GET Product yang memiliki Time to live (TTL) **900** second. Hit pertama akan melakukan pengambilan dari database dan akan disimpan di redis dengan key `product`, untuk hit selanjutnya akan melakukan pengambilan data dari redis dengan key `product`. Ketika proses insert data maka redis pada key `product` akan di flush.

Metode sort menggunakan fungsi [sorted](https://docs.python.org/3/howto/sorting.html) pada python, lebih efisien dibanding pada saat query order_by database, dan data yg di cache di redis tidak terlalu kompleks, karena hanya terdapat 1 data saja.

----

### Public postman documentation : [Click](https://documenter.getpostman.com/view/5040642/UVsG18xG)

### Method GET : <br />
Example : http://127.0.0.1:8000/product?sort=date&reverse=true

#### Parameter :
| Sort                                         |    Reverse    |
|----------------------------------------------|:-------------:|
| `date` merupakan sorting berdasarkan tanggal | jika reverse `true` maka diurutkan berdasarkan create date terbaru, jika `false` diurutkan berdasarkan create date terdahulu |
| `price` merupakan sorting berdasarkan harga  |   jika reverse `true` maka diurutkan berdasarkan harga termahal, jika `false` diurutkan berdasarkan harga termurah    |
| `name` merupakan sorting berdasarkan nama    |   jika reverse `false` maka diurutkan berdasarkan (A-Z) jika reverse `true` maka diurutkan berdasarkan (Z-A)    |

### Method POST : <br />
Example : http://127.0.0.1:8000/product

#### Body Raw (Json):
{
    "name": "Apple iPhone 13",
    "description": "iPhone",
    "price": 13000000,
    "quantity": 53
}

----

### Schema Database `model.py` :
Table Name : `product`

| Field        |              Tipe Data               |
|--------------|:------------------------------------:|
| product_id   | Integer, Primary Key, Auto Increment |
| name         |               Varchar                |
| description  |               Varchar                |
| price        |               Integer                |
| quantity     |               Integer                |
| created_date |               DateTime               |

----

### Menjalankan Aplikasi :

1. Menjalankan aplikasi : `docker-compose up --build`
2. Menjalankan Migration Database (terdapat 2 cara): 
   1. Inside Container
      1. docker exec -it erajayagroup_app_1 ash
      2. flask db init
      3. flask db migrate
      4. flask db upgrade
   2. Outside Container
      1. docker exec -it erajayagroup_app_1 flask db init
      2. docker exec -it erajayagroup_app_1 flask db migrate
      3. docker exec -it erajayagroup_app_1 flask db upgrade

### Deploy di environment production (Docker/Kubernetes) :
Pada file `Dockerfile` merupakan base image dari aplikasi, untuk melanjutkan tahap deployment production Dockerfile ini bisa dilakukan build dan push ke repository docker, selanjutnya pada kubernetes atau docker bisa dilakukan build image kembali dengan base image (From) yang telah kita push ke repository docker tadi dan ditambahkan [ENTRYPOINT](https://www.cloudbees.com/blog/understanding-dockers-cmd-and-entrypoint-instructions) uwsgi / asgi / gunicorn / uvicorn, environment variable yg dibutuhkan dan nginx (jika dibutuhkan).