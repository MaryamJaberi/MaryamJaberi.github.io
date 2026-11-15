/* Human-story stops for the atlas timeline, linked to the Persian wiki (tabar/).
   Inserted between the Eocene and the Holocene. Each stop carries English and Persian text. */
(function () {
  var E = window.EARTH_ERAS;
  if (!E) return;
  var W = "tabar/index.html#/a/";
  var stops = [
    {after: "eocene", id: "hominins-split", yearLabel: "7 million years ago", shortLabel: "7 mya", title: "Our Lineage Splits from the Chimpanzees'", epoch: "Late Miocene", category: "humans", map: "modern",
     climate: "Africa is drying. Forests break into woodland mosaics.", geology: "Continents close to their modern positions. The East African Rift is deepening.",
     plants: "Woodland and grassland expand at the expense of closed forest.", animals: "Apes are declining in Eurasia; in Africa our last common ancestor with chimpanzees lives.",
     humans: "Earliest possible hominins, such as Sahelanthropus in Chad, show hints of upright walking.", scienceThen: "Genetic clocks and fossils from Chad, Kenya, and Ethiopia date the split to roughly 7 to 6 million years ago.",
     sources: "Sahelanthropus, Orrorin, Ardipithecus finds.", uncertainty: "Which early fossils are true hominins is still argued.",
     titleFa: "جدایی تبار ما از شامپانزه‌ها", yearLabelFa: "۷ میلیون سال پیش", epochFa: "میوسن پسین",
     climateFa: "آفریقا خشک‌تر می‌شود و جنگل‌ها تکه‌تکه می‌شوند.", geologyFa: "قاره‌ها نزدیک جای امروزشان‌اند و دره‌ٔ کافتی شرق آفریقا عمیق‌تر می‌شود.",
     plantsFa: "جنگل انبوه جایش را به بیشه و علفزار می‌دهد.", animalsFa: "نیای مشترک ما و شامپانزه‌ها در آفریقا زندگی می‌کند.",
     humansFa: "نخستین انسان‌تباران احتمالی، مثل ساحل‌انسان چادی، نشانه‌هایی از راه رفتن روی دو پا دارند.", scienceThenFa: "ساعت ژنتیکی و سنگواره‌های چاد، کنیا و اتیوپی جدایی را حدود ۷ تا ۶ میلیون سال پیش می‌گذارند.",
     wiki: "hominins"},
    {after: "hominins-split", id: "australopiths", yearLabel: "3.2 million years ago", shortLabel: "3.2 mya", title: "Lucy's World: Upright Apes", epoch: "Pliocene", category: "humans", map: "modern",
     climate: "Warmer than today, but cooling toward the ice ages.", geology: "The Isthmus of Panama is closing; ocean currents are reorganizing.",
     plants: "Savanna woodlands across East and South Africa.", animals: "Big cats, hyenas, early elephants, and many antelopes.",
     humans: "Australopithecus afarensis walks upright with a small brain; Laetoli footprints date to about 3.7 million years ago.", scienceThen: "Lucy was found at Hadar, Ethiopia, in 1974.",
     sources: "Hadar; Laetoli; Lomekwi stone tools (3.3 mya).", uncertainty: "Who made the first stone tools is uncertain.",
     titleFa: "جهان لوسی: میمون‌های راست‌قامت", yearLabelFa: "۳٫۲ میلیون سال پیش", epochFa: "پلیوسن",
     climateFa: "گرم‌تر از امروز، اما رو به سرد شدن به سوی عصر یخبندان.", geologyFa: "تنگهٔ پاناما در حال بسته شدن است و جریان‌های اقیانوسی دگرگون می‌شوند.",
     plantsFa: "ساوانا و بیشه در شرق و جنوب آفریقا.", animalsFa: "گربه‌سانان بزرگ، کفتارها، فیل‌های نخستین و آنتلوپ‌های فراوان.",
     humansFa: "استرالوپیتکوس آفارنسیس با مغزی کوچک روی دو پا راه می‌رود؛ ردپاهای لائتولی حدود ۳٫۷ میلیون سال پیش‌اند.", scienceThenFa: "لوسی در ۱۹۷۴ در هادار اتیوپی پیدا شد.",
     wiki: "australopithecus"},
    {after: "australopiths", id: "erectus-out", yearLabel: "1.8 million years ago", shortLabel: "1.8 mya", title: "Homo erectus Leaves Africa", epoch: "Early Pleistocene", category: "humans", map: "modern",
     climate: "Ice-age cycles begin to swing between cold and warm.", geology: "Modern continents; sea level rises and falls with the ice.",
     plants: "Grasslands spread widely in Africa and Asia.", animals: "Saber-toothed cats, giant hyenas, early horses and elephants across Eurasia.",
     humans: "Homo erectus, with a modern-like body and bigger brain, reaches Dmanisi in Georgia and later Java and China. Acheulean hand axes appear.",
     scienceThen: "Dmanisi skulls (1990s onward) showed humans left Africa early and small-brained.", sources: "Dmanisi; Java; Zhoukoudian.", uncertainty: "Earlier dispersals may exist.",
     titleFa: "انسان راست‌قامت از آفریقا بیرون می‌رود", yearLabelFa: "۱٫۸ میلیون سال پیش", epochFa: "پلیستوسن پیشین",
     climateFa: "چرخه‌های یخبندان و گرما آغاز می‌شود.", geologyFa: "قاره‌های امروزی؛ سطح دریا با یخ بالا و پایین می‌رود.",
     plantsFa: "علفزارها در آفریقا و آسیا گسترده می‌شوند.", animalsFa: "گربه‌های دندان‌شمشیری، کفتارهای غول‌پیکر و فیل‌های نخستین در اوراسیا.",
     humansFa: "انسان راست‌قامت با بدنی شبیه ما و مغزی بزرگ‌تر به دمانیسی گرجستان و سپس جاوه و چین می‌رسد. تبرهای دستی آشولی پیدا می‌شوند.", scienceThenFa: "جمجمه‌های دمانیسی (از دههٔ ۱۹۹۰) نشان داد انسان زود و با مغزی کوچک از آفریقا بیرون رفت.",
     wiki: "homo-erectus"},
    {after: "erectus-out", id: "neanderthal-world", yearLabel: "100,000 years ago", shortLabel: "100 kya", title: "A World of Several Humans", epoch: "Late Pleistocene", category: "humans", map: "iceage",
     climate: "The last interglacial ends; ice builds again.", geology: "Modern continents; sea level falling.",
     plants: "Steppe and open woodland across Eurasia.", animals: "Mammoths, cave bears, woolly rhinos.",
     humans: "Neanderthals in Europe and West Asia including the Zagros, Denisovans in Asia, Homo floresiensis and Homo luzonensis on islands, Homo sapiens in Africa and briefly the Levant. Neanderthals bury some of their dead.", scienceThen: "Ancient DNA since 2010 shows these groups interbred.",
     sources: "Shanidar; Skhul and Qafzeh; Denisova Cave.", uncertainty: "How the groups met is reconstructed from scattered sites.",
     titleFa: "جهانی با چند گونهٔ انسان", yearLabelFa: "۱۰۰ هزار سال پیش", epochFa: "پلیستوسن پسین",
     climateFa: "میان‌یخچالی پایان می‌یابد و یخ دوباره گسترش می‌یابد.", geologyFa: "قاره‌های امروزی؛ سطح دریا رو به پایین.",
     plantsFa: "استپ و بیشهٔ باز در سراسر اوراسیا.", animalsFa: "ماموت، خرس غار، کرگدن پشمالو.",
     humansFa: "نئاندرتال‌ها در اروپا و غرب آسیا از جمله زاگرس، دنیسووایی‌ها در آسیا، انسان فلورسی و لوزونی در جزیره‌ها، و انسان خردمند در آفریقا و گاه در لوانت. نئاندرتال‌ها برخی مردگانشان را دفن می‌کنند.", scienceThenFa: "DNA باستانی از ۲۰۱۰ نشان داد این گروه‌ها با هم آمیزش داشتند.",
     wiki: "neanderthal"},
    {after: "neanderthal-world", id: "sapiens-spread", yearLabel: "50,000 years ago", shortLabel: "50 kya", title: "Out of Africa, Across the World", epoch: "Late Pleistocene", category: "humans", map: "iceage",
     climate: "Cold, unstable glacial climate with lower seas.", geology: "Sunda and Sahul shelves are partly dry land.",
     plants: "Steppe-tundra in the north, savanna in the south.", animals: "Megafauna on every continent, soon to decline where humans arrive.",
     humans: "Homo sapiens spreads through Arabia and the Iranian Plateau to South Asia, Australia, and Europe; Neanderthals vanish around 40,000 years ago.", scienceThen: "Genomes place most non-African ancestry in one main dispersal; the Persian Plateau is proposed as a hub.",
     sources: "Out-of-Africa genetics; Lake Mungo; Bacho Kiro.", uncertainty: "Exact routes and dates are actively revised.",
     titleFa: "خروج از آفریقا و پراکنده شدن در جهان", yearLabelFa: "۵۰ هزار سال پیش", epochFa: "پلیستوسن پسین",
     climateFa: "آب‌وهوای سرد و ناپایدار یخچالی با دریاهای پایین‌تر.", geologyFa: "فلات‌های ساندا و ساحول بخشی خشکی‌اند.",
     plantsFa: "استپ‌تندرا در شمال و ساوانا در جنوب.", animalsFa: "جانوران بزرگ در همهٔ قاره‌ها، که جایی که انسان می‌رسد رو به کاهش می‌روند.",
     humansFa: "انسان خردمند از راه عربستان و فلات ایران به جنوب آسیا، استرالیا و اروپا می‌رسد؛ نئاندرتال‌ها حدود ۴۰ هزار سال پیش ناپدید می‌شوند.", scienceThenFa: "ژنوم‌ها بیشتر تبار غیرآفریقایی را به یک خروج اصلی می‌رسانند و فلات ایران پایگاهی احتمالی است.",
     wiki: "out-of-africa"},
    {after: "lgm", id: "younger-dryas", yearLabel: "12,900 years ago", shortLabel: "12.9 kya", title: "The Younger Dryas Chill", epoch: "Late Glacial", category: "climate", map: "iceage",
     climate: "A sudden return to near-glacial cold for about 1,200 years.", geology: "Ice sheets shrinking; seas rising.",
     plants: "Wild cereals retreat, then return in the Fertile Crescent.", animals: "Many large mammals disappear across the Americas and northern Eurasia.",
     humans: "Natufian villagers in the Levant and Zagros foragers face the cold; some begin cultivating wild cereals.", scienceThen: "Named from the tundra flower Dryas octopetala in pollen records.",
     sources: "Ice cores; Natufian archaeology.", uncertainty: "Its cause is still debated.",
     titleFa: "سرمای دریاس جوان", yearLabelFa: "۱۲٬۹۰۰ سال پیش", epochFa: "پایان یخچالی",
     climateFa: "بازگشت ناگهانی سرمای نزدیک به یخبندان برای حدود ۱۲۰۰ سال.", geologyFa: "یخ‌ها آب می‌شوند و دریاها بالا می‌آیند.",
     plantsFa: "غلات وحشی در هلال حاصلخیز عقب می‌نشینند و سپس بازمی‌گردند.", animalsFa: "بسیاری از پستانداران بزرگ در آمریکا و شمال اوراسیا ناپدید می‌شوند.",
     humansFa: "روستانشینان ناتوفی در لوانت و گردآورندگان زاگرس با سرما روبه‌رو می‌شوند؛ برخی کاشت غلات وحشی را آغاز می‌کنند.", scienceThenFa: "نامش از گل تندرایی «دریاس» در دانه‌های گردهٔ رسوبات است.",
     wiki: "younger-dryas"},
    {after: "younger-dryas", id: "neolithic", yearLabel: "10,000 years ago", shortLabel: "10 kya", title: "First Farmers of the Zagros and the Levant", epoch: "Early Holocene", category: "humans", map: "modern",
     climate: "The Holocene warms and stabilizes.", geology: "Coasts approach modern shapes.",
     plants: "Wheat and barley cultivated at sites like Chogha Golan.", animals: "Goats herded at Ganj Dareh in the Zagros; sheep, cattle, and pigs follow.",
     humans: "Permanent villages; the Zagros is one of the hearths of farming.", scienceThen: "Re-study of Ganj Dareh goat bones dated herding to about 10,000 years ago.",
     sources: "Ganj Dareh; Chogha Golan; Ali Kosh.", uncertainty: "Domestication was a long process in several places.",
     titleFa: "نخستین کشاورزان زاگرس و لوانت", yearLabelFa: "۱۰ هزار سال پیش", epochFa: "هولوسن پیشین",
     climateFa: "هولوسن گرم و پایدار می‌شود.", geologyFa: "خط ساحل‌ها به شکل امروز نزدیک می‌شوند.",
     plantsFa: "گندم و جو در محوطه‌هایی مثل چغاگلان کشت می‌شوند.", animalsFa: "بز در گنج‌دره در زاگرس گله‌داری می‌شود؛ گوسفند، گاو و خوک در پی آن.",
     humansFa: "روستاهای پایدار؛ زاگرس یکی از کانون‌های کشاورزی است.", scienceThenFa: "بازبینی استخوان‌های بز گنج‌دره گله‌داری را حدود ۱۰ هزار سال پیش نشان داد.",
     wiki: "neolithic"}
  ];
  stops.forEach(function (s) {
    if (E.some(function (e) { return e.id === s.id; })) return;
    var i = E.findIndex(function (e) { return e.id === s.after; });
    delete s.after;
    s.wikiUrl = W + s.wiki;
    E.splice(i + 1, 0, s);
  });
  ["lgm", "holocene"].forEach(function (id) {
    var e = E.find(function (x) { return x.id === id; });
    if (e) e.wikiUrl = W + (id === "lgm" ? "lgm" : "sedentism");
  });
})();
