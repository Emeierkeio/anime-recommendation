Data Directory
================================================

API
----
Using API, we obtained several important pieces of information of all the souls in the AniApi database (more than 14000), and, for convenience, we divided them into several tables:

* The first file contains the most important informations of every anime (id, title, year, episodes count and duration, ...)

.. list-table:: anime_informations.csv [rows: 14.356]
   :header-rows: 1

   * - id
     - en_title
     - season_year
     - episodes_count
     - episode_duration
     - format_destination
     - release_status
   * - 39486
     - Gintama: THE FINAL
     - 2021
     - 1
     - 104
     - movie
     - finished
   * - 42938
     - Fruits Basket: The Final
     - 2021
     - 13
     - 24
     - tv
     - finished
   * - 28977
     - Gintama°
     - 2015
     - 51
     - 24
     - tv
     - finished
   * - ...
     - ...
     - ...
     - ...
     - ...
     - ...
     - ...
   * - 50612
     - Dr. STONE: Ryuusui
     - 2022
     - 1
     - 
     - special
     - not yet released

* The second file contains the genres of every anime, each id is repeated for every genre that features the anime.

.. list-table:: anime_genres.csv [rows: 84.419]
   :header-rows: 1

   * - id
     - genre
   * - 39486
     - Action
   * - 39486
     - Comedy
   * - 39486
     - Drama
   * - ...
     - ...
   * - 50612
     - Post-Apocalyptic

* The third file contains the description of every anime.


.. list-table:: anime_descriptions.csv [rows: 14.356]
   :header-rows: 1

   * - id
     - description
   * - 39486
     - Gintama The Final is the 3rd and final film adaptation of the remainder of the Silver Soul Arc
   * - 42938
     - 
   * - 28977
     - Gintoki, Shinpachi, and Kagura return as the fun-loving but broke members of the Yorozuya team!...
   * - ...
     - ...
   * - 50612
     - A television special that is set after the second season and will center around Ryuusui Nanami.


Scraping
--------

In order to increase the amount of data at our disposal, we have chosen, through the scraping tool, to obtain information from one of the most famous sites dedicated to anime, namely myanimelist.net, we divided them into several tables:

* The first file contains the informations about studios and producer:

.. list-table:: animeStudiosandDirector.csv [rows: 13.077]
   :header-rows: 1

   * - id
     - studios
     - director
   * - 39486
     - Bandai Namco Pictures
     - Fujita Youichi
   * - 42938
     - TMS Entertainment
     - Ibata Yoshihide
   * - 28977
     - Bandai Namco Pictures
     - Fujita Youichi
   * - ...
     - ...
     - ...
   * - 50612
     - TMS Entertainment
     - Boichi

* The second file contains the informations about reviews and votes:

.. list-table:: reviews.csv [rows: 21.370]
   :header-rows: 1

   * - id
     - overall
     - text
   * - 39486
     - 10
     - Overall 10   Story 10   Animation 10   Sound 10   Character 10   Enjoyment 10  Its finally over. The story that I...
   * - 39486
     - 4
     - Overall 4   Story 0   Animation 0   Sound 0   Character 0   Enjoyment 0  To be honest, i'm disappointed.   Ah, Gintama,...
   * - 39486
     - 10
     - Overall 10   Story 9   Animation 8   Sound 10   Character 10   Enjoyment 10  This movie has everything that makes a classic Gintama: parody, toile...
   * - ...
     - ...
     - ...
   * - 50612
     - 8
     -  Overall 8   Story 8   Animation 9   Sound 10   Character 8   Enjoyment 9  This review will contain NO SPOILERS.   First of al...

* The third file contains the informations about recommendations, it contains the couple (id anime, id recommendated anime)

.. list-table:: recommendations.csv [rows: 149.422]
   :header-rows: 1

   * - id
     - recommendation
   * - 39486
     - 40211
   * - 39486
     - 3002
   * - 39486
     - 759
   * - ...
     - ...
   * - 50612
     - 16662

* The fourth file contains the cleaned informations about reviews, different valuations are divided (Overall, Story, Animation, Sound, Charachter, Enjoyment)

.. list-table:: cleanedReviews.csv [rows: 21.366]
   :header-rows: 1

   * - id
     - overall
     - story
     - animation
     - sound
     - charachter
     - enjoyment
     - text
   * - 39486
     - 10
     - 10
     - 10
     - 10
     - 10
     - 10
     - Its finally over. The story that I learned so many things from, the story which had a deep impression...
   * - 39486
     - 4
     - 0
     - 0
     - 0
     - 0
     - 0
     - To be honest, i'm disappointed. Ah, Gintama, you used to be great a long time ago, what happened?...
   * - 39486
     - 10
     - 9
     - 8
     - 10
     - 10
     - 10
     - This movie has everything that makes a classic Gintama: parody, toilet humor, drama, sword action, tears and...
   * - ...
     - ...
     - ...
     - ...
     - ...
     - ...
     - ...
     - ...
   * - 29727
     - 8
     - 8
     - 9
     - 10
     - 8
     - 9
     - This review will contain NO SPOILERS. First of all, I was totally surprised when I saw the number of people who...
