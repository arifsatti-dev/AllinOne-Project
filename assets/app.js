/* All In One – client-side logic
 * - Home: live search + category chips
 * - Image tools (compress / convert) run 100% in the browser (files never leave the device)
 * - PDF tools (JPG to PDF, Merge PDF) run in the browser with pdf-lib
 * - Downloaders and PDF<->Word need a backend: set window.ALLINONE_API in assets/config.js
 */
(function () {
  "use strict";

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  function fmtSize(b) {
    if (b < 1024) return b + " B";
    if (b < 1048576) return (b / 1024).toFixed(1) + " KB";
    return (b / 1048576).toFixed(2) + " MB";
  }
  function setStatus(msg, ok) {
    var el = $("#status");
    if (!el) return;
    el.textContent = msg || "";
    el.style.color = ok ? "#16a34a" : "";
  }
  function saveBlob(blob, name) {
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1500);
  }
  function baseName(n) { return n.replace(/\.[^.]+$/, ""); }

  /* ---------- Home: search + chips ---------- */
  var search = $("#toolSearch");
  if (search) {
    var cards = $$(".tool[data-cat]");
    var cat = "all";
    var apply = function () {
      var q = search.value.trim().toLowerCase();
      cards.forEach(function (c) {
        var hit = (!q || c.textContent.toLowerCase().indexOf(q) > -1) && (cat === "all" || c.dataset.cat === cat);
        c.hidden = !hit;
      });
    };
    search.addEventListener("input", apply);
    $$(".chip").forEach(function (ch) {
      ch.addEventListener("click", function () {
        $$(".chip").forEach(function (x) { x.classList.remove("active"); });
        ch.classList.add("active");
        cat = ch.dataset.cat;
        apply();
      });
    });
  }

  /* ---------- Drop zone helper ---------- */
  function setupDrop(onFiles) {
    var drop = $(".drop"), input = $("#fileInput");
    if (!drop || !input) return;
    drop.addEventListener("click", function () { input.click(); });
    drop.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); input.click(); } });
    ["dragenter", "dragover"].forEach(function (ev) {
      drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.add("over"); });
    });
    ["dragleave", "drop"].forEach(function (ev) {
      drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.remove("over"); });
    });
    drop.addEventListener("drop", function (e) { onFiles(Array.prototype.slice.call(e.dataTransfer.files)); });
    input.addEventListener("change", function () { onFiles(Array.prototype.slice.call(input.files)); input.value = ""; });
  }

  function loadImage(file) {
    return new Promise(function (res, rej) {
      var url = URL.createObjectURL(file), img = new Image();
      img.onload = function () { res({ img: img, url: url }); };
      img.onerror = function () { URL.revokeObjectURL(url); rej(new Error("Could not read " + file.name)); };
      img.src = url;
    });
  }
  function toBlob(canvas, type, q) {
    return new Promise(function (res) { canvas.toBlob(res, type, q); });
  }
  function addResult(host, o) {
    var d = document.createElement("div");
    d.className = "res";
    d.innerHTML = '<img alt="">' +
      '<div class="nm"></div><div class="sz"></div>' +
      (o.saved ? '<div class="saved"></div>' : "") +
      '<div class="row"><button class="btn">Download</button></div>';
    $("img", d).src = o.thumb;
    $(".nm", d).textContent = o.name;
    $(".sz", d).textContent = o.info;
    if (o.saved) $(".saved", d).textContent = o.saved;
    $(".btn", d).addEventListener("click", function () { saveBlob(o.blob, o.name); });
    host.appendChild(d);
  }

  /* ---------- Tool modules ---------- */
  var tool = document.body.dataset.tool;

  if (tool === "image-compress" || tool === "image-convert") {
    var results = $("#results");
    var run = async function (files) {
      files = files.filter(function (f) { return /^image\//.test(f.type); });
      if (!files.length) { setStatus("Please choose image files (JPG, PNG, WEBP)."); return; }
      results.innerHTML = "";
      setStatus("Working…");
      var quality = tool === "image-compress" ? parseInt($("#quality").value, 10) / 100 : 0.92;
      var maxW = tool === "image-compress" ? parseInt($("#maxw").value, 10) : 0;
      var fmt = $("#format").value;
      var done = 0;
      for (var i = 0; i < files.length; i++) {
        try {
          var f = files[i], L = await loadImage(f);
          var w = L.img.naturalWidth, h = L.img.naturalHeight;
          if (maxW && w > maxW) { h = Math.round(h * maxW / w); w = maxW; }
          var c = document.createElement("canvas");
          c.width = w; c.height = h;
          var ctx = c.getContext("2d");
          if (fmt === "image/jpeg") { ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, w, h); }
          ctx.drawImage(L.img, 0, 0, w, h);
          var blob = await toBlob(c, fmt, quality);
          if (!blob) throw new Error("This browser cannot export " + fmt);
          var ext = fmt === "image/jpeg" ? "jpg" : fmt === "image/webp" ? "webp" : "png";
          var pct = Math.round((1 - blob.size / f.size) * 100);
          addResult(results, {
            thumb: L.url,
            name: baseName(f.name) + (tool === "image-compress" ? "-compressed." : ".") + ext,
            info: fmtSize(f.size) + " → " + fmtSize(blob.size),
            saved: tool === "image-compress" ? (pct > 0 ? "Saved " + pct + "%" : "Already well optimised") : "",
            blob: blob
          });
          done++;
        } catch (e) { setStatus(e.message); }
      }
      setStatus(done + " file" + (done === 1 ? "" : "s") + " ready. Nothing was uploaded – it all happened in your browser.", true);
    };
    setupDrop(run);
    var q = $("#quality"), qv = $("#qval");
    if (q) q.addEventListener("input", function () { qv.textContent = q.value + "%"; });
  }

  if (tool === "jpg-to-pdf" || tool === "merge-pdf") {
    var queue = [];
    var list = $("#results");
    var render = function () {
      list.innerHTML = "";
      queue.forEach(function (f, i) {
        var d = document.createElement("div");
        d.className = "res";
        d.innerHTML = '<div class="nm"></div><div class="sz"></div><div class="row"><button class="btn ghost" data-a="up">↑</button><button class="btn ghost" data-a="down">↓</button><button class="btn ghost" data-a="rm">Remove</button></div>';
        $(".nm", d).textContent = (i + 1) + ". " + f.name;
        $(".sz", d).textContent = fmtSize(f.size);
        d.addEventListener("click", function (e) {
          var a = e.target.dataset && e.target.dataset.a;
          if (a === "rm") queue.splice(i, 1);
          else if (a === "up" && i > 0) { var t = queue[i - 1]; queue[i - 1] = queue[i]; queue[i] = t; }
          else if (a === "down" && i < queue.length - 1) { var u = queue[i + 1]; queue[i + 1] = queue[i]; queue[i] = u; }
          else return;
          render();
        });
        list.appendChild(d);
      });
      $("#make").disabled = queue.length === 0;
    };
    setupDrop(function (files) {
      var want = tool === "merge-pdf" ? /pdf$/i : /^image\/(jpeg|png)$/;
      files.forEach(function (f) {
        if (tool === "merge-pdf" ? (f.type === "application/pdf" || /\.pdf$/i.test(f.name)) : want.test(f.type)) queue.push(f);
      });
      setStatus(queue.length ? "" : (tool === "merge-pdf" ? "Please choose PDF files." : "Please choose JPG or PNG images."));
      render();
    });
    $("#make").addEventListener("click", async function () {
      if (!window.PDFLib) { setStatus("PDF engine failed to load. Check your internet connection and refresh."); return; }
      setStatus("Creating PDF…");
      try {
        var PDFDocument = window.PDFLib.PDFDocument;
        var out = await PDFDocument.create();
        for (var i = 0; i < queue.length; i++) {
          var bytes = await queue[i].arrayBuffer();
          if (tool === "merge-pdf") {
            var src = await PDFDocument.load(bytes, { ignoreEncryption: true });
            var pages = await out.copyPages(src, src.getPageIndices());
            pages.forEach(function (p) { out.addPage(p); });
          } else {
            var img = queue[i].type === "image/png" ? await out.embedPng(bytes) : await out.embedJpg(bytes);
            var page = out.addPage([img.width, img.height]);
            page.drawImage(img, { x: 0, y: 0, width: img.width, height: img.height });
          }
        }
        var data = await out.save();
        saveBlob(new Blob([data], { type: "application/pdf" }), tool === "merge-pdf" ? "merged.pdf" : "images.pdf");
        setStatus("Done! Your PDF was downloaded.", true);
      } catch (e) {
        setStatus("Sorry, something went wrong: " + e.message);
      }
    });
    render();
  }

  /* ---------- Backend-powered tools ---------- */
  var API = (window.ALLINONE_API || "").replace(/\/$/, "");

  function needBackend() {
    setStatus("This tool needs the backend service. Open assets/config.js and set ALLINONE_API (see README).");
  }

  if (tool === "downloader") {
    var form = $("#dlForm"), out = $("#results");
    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      var url = $("#dlUrl").value.trim();
      var platform = document.body.dataset.platform;
      out.innerHTML = "";
      if (!/^https?:\/\//i.test(url)) { setStatus("Please paste a full link starting with https://"); return; }
      if (!API) { needBackend(); return; }
      setStatus("Fetching…");
      try {
        var r = await fetch(API + "/download", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ url: url, platform: platform })
        });
        if (!r.ok) throw new Error("Server said " + r.status);
        var data = await r.json();
        (data.links || []).forEach(function (l) {
          var d = document.createElement("div");
          d.className = "res";
          d.innerHTML = '<div class="nm"></div><div class="row"><a class="btn" rel="noopener" target="_blank">Download</a></div>';
          $(".nm", d).textContent = l.label || data.title || "File";
          $("a", d).href = l.url;
          out.appendChild(d);
        });
        setStatus((data.links || []).length ? "Ready – choose a file below." : "No downloadable file was found for that link.", !!(data.links || []).length);
      } catch (err) {
        setStatus("Could not fetch that link: " + err.message);
      }
    });
  }

  if (tool === "doc-convert") {
    var which = document.body.dataset.convert; // pdf-to-word | word-to-pdf
    setupDrop(async function (files) {
      var f = files[0];
      if (!f) return;
      if (!API) { needBackend(); return; }
      setStatus("Converting " + f.name + "…");
      try {
        var fd = new FormData();
        fd.append("file", f);
        var r = await fetch(API + "/convert/" + which, { method: "POST", body: fd });
        if (!r.ok) throw new Error("Server said " + r.status);
        var blob = await r.blob();
        saveBlob(blob, baseName(f.name) + (which === "pdf-to-word" ? ".docx" : ".pdf"));
        setStatus("Done! Your file was downloaded.", true);
      } catch (err) {
        setStatus("Conversion failed: " + err.message);
      }
    });
  }
})();
