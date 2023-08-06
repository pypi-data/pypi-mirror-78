let mix = require("laravel-mix")

mix.setPublicPath("../static")

mix.ts("ts/karvi.ts", "karvi/js")
mix.sass("sass/karvi.sass", "karvi/css")
