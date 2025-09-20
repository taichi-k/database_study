# database_study

## DB比較表
|DB名|種類|ライセンス|主な特徴|主な用途|サポート言語|
|---|---|---|---|---|---|
|MySQL|RDBMS|GPL|オープンソース、トランザクション重視、集合論的に考える|ウェブアプリケーション、eコマース|SQL|
|PostgreSQL|RDBMS|PostgreSQL License|高度な機能、拡張性、ACID準拠、GISサポート|データ分析、地理情報システム|SQL|
|SQLite|RDBMS|Public Domain|軽量、組み込み型、サーバーレス、自己完結型|モバイルアプリ、組み込みシステム|SQL|
|MongoDB|NoSQL|SSPL|ドキュメント指向け、スキーマレス、水平スケーリングが容易|ビッグデータ、リアルタイム分析|JavaScript,Python,Java|
|Cassandra|NoSQL|Apache License 2.0|高可用性、スケーラビリティ、分散型データベース|大規模データストア、IoT|CQL(Cassandra Query Language)|
|Redis|NoSQL|BSD|インメモリデータストア、高速、データ構造サーバー|キャッシュ、セッション管理|C,Python,Java,Ruby|
|MariaDB|RDBMS|GPL|MySQLのフォーク、高性能、拡張性、オープンソース|ウェブアプリケーション、eコマース|SQL|
|Neo4j|グラフDB|GPL|グラフデータモデル、関係性のクエリが得意|ソーシャルネットワーク、推薦システム|Cypher|
|Oracle Database|RDBMS|Proprietary|高度なセキュリティ、スケーラビリティ、豊富な機能セット|大規模エンタープライズシステム|PL/SQL|
|Microsoft SQL Server|RDBMS|Proprietary|高性能、セキュリティ、BIツールとの統合が強力|エンタープライズアプリケーション|T-SQL|
|Amazon Aurora|RDBMS|Proprietary|MySQL/PostgreSQL互換、クラウドネイティブ、高可用性|クラウドアプリケーション|SQL|
|Amazon DynamoDB|NoSQL|Proprietary|フルマネージド、スケーラブル、低レイテンシ|IoT、モバイル、ゲーム|Java,JavaScript,Python,他|
|Amazon Redshift|DWH|Proprietary|高速分析、ペタバイト級データウェアハウス|BI、データ分析|SQL|
|Google BigQuery|DWH|Proprietary|サーバーレス、超高速分析、スケーラブル|BI、データ分析|SQL|
|Google Cloud Spanner|RDBMS|Proprietary|グローバル分散、強整合性、スケーラビリティ|ミッションクリティカルなアプリ|SQL|
|Google Cloud Firestore|NoSQL|Proprietary|ドキュメント指向、リアルタイム同期、スケーラブル|モバイル、ウェブアプリ|JavaScript,Python,Go,他|
|DuckDB|RDBMS|MIT|組み込み型、列指向、高速分析、サーバーレス|データ分析、ローカル分析|SQL|


# MySQL

みんな大好きMySQL。
トランザクションが必要な時や、特に制約がなく小〜中規模なアプリならこれでいいかも。
インデックスを適切に張れば、Readも高速。Writeはトランザクションなどの兼ね合いでちょい重め。

# PostgreSQL

先進的なオープンRDBMS。
SQL標準に忠実。OLTPだけでなくOLAP用としても優秀。金融系で使われたり。
MVCCにより、複数バージョンを保持しながら同時実行を行う。VACUUMでゴミ回収が必須。

# SQLite

組み込みなのでサーバとか立てなくてOK。
軽いアプリケーションにはGood。データ量が膨大だったり書き込み負荷が高い場合は合わない。

# MongoDB

ドキュメントDB。
JSONで保存していくので、JOINとか不要で一発で情報取れる。Arrayとかも格納できる。
水平スケーリングが得意な理由としては、「シャーディング機能が標準で搭載されている」「スキーマレス」などがある。
自動バランシングや、レプリカセットとの組み合わせ、mongosルーターによる自動シャード管理が便利。
[Atlas](https://www.mongodb.com/atlas)を使えばWebUIでセットアップや分析などができる。

# DynamoDB

基本はKey-Valueストアに近い。
MongoDBに似てるけど、こっちはマネージドなので運用面をほとんど気にしなくて良い（R/Wのスループット、キャパシティを設定するだけ）。
MongoDBに比べると検索クエリの表現力が低い。
超大量データ＆高スループットな書き込みに便利。

# Cassandra

分散DB。
世界規模のサービスなどで使われる。列指向でOLAP系。
勝手にシャーディングや自動リバランシングもやってくれる。UUIDなどを用いて、Consistent Hashアルゴリズムによる。
RF（いくつのノードに書き込みするか）と、Consistency Level（いくつのノードの書き込み成功を待つか）などを設定する。
分散DBと連番IDは相性が悪いのであまり使わない。utilにuuid_from_time()とかがある。

# Redis

キャッシュやメッセージキュー的な用途で使う。
一応RedisJSONとかを使うと、ドキュメントDBっぽくも使える。
キャッシュできるところはキャッシュしていこう。

# MariaDB

MySQLとほぼ同様に扱える。MySQLの開発者がフォーク。

# Neo4j

グラフDB。グラフ構造で表しやすい、ネットワーク的なデータの扱いにgood。
例えば、フォロー関係のあるユーザネットワークの表現など。
WebUIでグリグリとグラフを見れる。

# duckDB

最近キテるらしい。
sqlite同様、組み込みで、データフォーマットが柔軟。いろいろ遊びたい。
自動で並列化とか、SIMD（Single Instruction, Multiple Data）の活用により、大規模データの集計は、Pandasで読み込むより速いらしい。
ベクトル化エンジンであり、列をベクトルとして扱う。


# Redshift

いわゆるDWH。
ETLを通して専用ストレージ（Redshiftクラスタ）にデータを格納し、分析を行う。
列指向・圧縮・並列処理により大規模分析が得意。大規模で頻繁に分析するならコレ。
クラスタの利用料金が時間でかかる。が、Redshift Serverlessもある。

# Athena

S3上のログデータなどを直接分析できる。
スキャン量に応じて従量課金。SQLを叩きミスすると無駄にコストをかけてしまい、ヒヤッとする。
Ad-hocな分析や、ログ・CSV/Parquet/JSONなどの解析に強い。
分析対象のデータを、ParquetやORC形式（列指向データ）にしておくのが鉄板。