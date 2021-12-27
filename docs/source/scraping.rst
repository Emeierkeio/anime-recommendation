Web Scraping Code
================================================

This section contains the documentation required to scrape informations from https://myanimelist.net/.

Overview
---------

.. autosummary::
   :toctree: generated

   webScraping
   dataCleaning

Functions
---------

.. autofunction:: webScraping.getId
.. autofunction:: webScraping.getPage
.. autofunction:: webScraping.getDirector
.. autofunction:: webScraping.getRatingAndReviews
.. autofunction:: webScraping.getRecommendations
.. autofunction:: webScraping.getStudios
.. autofunction:: webScraping.studiosandDirectorCsv
.. autofunction:: webScraping.recommendationsCsv
.. autofunction:: webScraping.removeFirstRow
.. autofunction:: webScraping.reviewsCsv

.. autofunction:: dataCleaning.cleanReviews
.. autofunction:: dataCleaning.digitsInLine
.. autofunction:: dataCleaning.evaluationsListtoString
.. autofunction:: dataCleaning.getEvaluations
.. autofunction:: dataCleaning.improveReviewText
