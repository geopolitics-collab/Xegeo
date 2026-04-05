const fs = require("fs");
const path = require("path");

const baseUrl = "https://fr.geopolo.com";

// dossier où sont tes pages
const pagesDir = "./";

// récupérer tous les fichiers html
const files = fs.readdirSync(pagesDir)
  .filter(file => file.endsWith(".html"));

// construire le sitemap
let urls = files.map(file => {
  let url = file === "index.html"
    ? baseUrl
    : `${baseUrl}/${file}`;

  return `
  <url>
    <loc>${url}</loc>
  </url>`;
}).join("");

const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>`;

// écrire le fichier sitemap.xml
fs.writeFileSync("sitemap.xml", sitemap);

console.log("✅ sitemap généré !");
