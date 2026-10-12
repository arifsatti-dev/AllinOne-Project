/* Backend connection (optional).
 * Image compressor, image converter, JPG to PDF and Merge PDF work with NO backend.
 * Downloader pages and PDF <-> Word need a server you control. When you have one, put its URL here:
 *   window.ALLINONE_API = "https://api.yourdomain.com";
 *
 * Expected endpoints:
 *   POST /download           JSON {url, platform}  ->  {title, links:[{label, url}]}
 *   POST /convert/pdf-to-word   multipart "file"  ->  .docx file
 *   POST /convert/word-to-pdf   multipart "file"  ->  .pdf file
 */
window.ALLINONE_API = "";
