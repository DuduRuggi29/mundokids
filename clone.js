const fs = require('fs');
const https = require('https');
const path = require('path');

const baseUrl = 'https://turminha-alfakids.online/';
const indexContent = fs.readFileSync('index.html', 'utf8');

// Match simple relative URLs in href or src or url()
const urlRegex = /(?:href|src|url)\s*=\s*['"]?([^'"\s<>)]+)['"\s<>)]?/gi;
let match;
const urls = new Set();

while ((match = urlRegex.exec(indexContent)) !== null) {
  let url = match[1];
  if (url.startsWith('data:') || url.startsWith('http') || url.startsWith('javascript:')) {
    continue;
  }
  // Remove hash fragment if it's there
  url = url.split('#')[0];
  if (url) {
    urls.add(url);
  }
}

// Ensure unique, maybe some are .woff2 format
const uniqueUrls = Array.from(urls);

function downloadFile(urlPath) {
  return new Promise((resolve, reject) => {
    // some paths might contain query strings or fragments, but they are stripped
    const fullUrl = baseUrl + urlPath;
    const dest = path.join(__dirname, urlPath);
    
    // Ensure directory exists
    const dir = path.dirname(dest);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    if (fs.existsSync(dest) && fs.statSync(dest).size > 0) {
      // file exists, skip
      resolve();
      return;
    }

    https.get(fullUrl, (res) => {
      if (res.statusCode === 200) {
        const file = fs.createWriteStream(dest);
        res.pipe(file);
        file.on('finish', () => {
          file.close(resolve);
        });
      } else {
        console.error(`Failed to download ${fullUrl}: ${res.statusCode}`);
        resolve(); // resolve anyway to continue
      }
    }).on('error', (err) => {
      console.error(`Error downloading ${fullUrl}: ${err.message}`);
      resolve();
    });
  });
}

async function scrape() {
  console.log(`Found ${uniqueUrls.length} assets to download...`);
  const promises = uniqueUrls.map(u => downloadFile(u));
  // Batch processing
  for (let i = 0; i < uniqueUrls.length; i += 10) {
    await Promise.all(uniqueUrls.slice(i, i + 10).map(downloadFile));
    console.log(`Finished ${Math.min(i + 10, uniqueUrls.length)} / ${uniqueUrls.length}`);
  }
  console.log('All assets downloaded.');
}

scrape();
