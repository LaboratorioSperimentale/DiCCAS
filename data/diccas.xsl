<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:tei="http://www.tei-c.org/ns/1.0"
  exclude-result-prefixes="tei">

  <xsl:output method="html" version="5" encoding="UTF-8" indent="yes"/>

  <!-- ============================================================ -->
  <!-- ROOT                                                          -->
  <!-- ============================================================ -->

  <xsl:template match="/">
    <html lang="en">
      <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>
          <xsl:value-of select="//tei:titleStmt/tei:title"/>
        </title>
        <style><![CDATA[
/* ── Base ── */
*, *::before, *::after { box-sizing: border-box; }

:root {
  --serif: Georgia, "Times New Roman", serif;
  --sans:  "Segoe UI", system-ui, sans-serif;
  --bg:         #fafaf8;
  --surface:    #ffffff;
  --border:     #e0ddd5;
  --muted:      #6b6459;
  --accent:     #5c4a1e;
  --link:       #3b6ea5;

  /* term subtype colours */
  --c-natural:    #2e7d32;
  --c-divine:     #6a1b9a;
  --c-military:   #b71c1c;
  --c-political:  #e65100;
  --c-social:     #0277bd;
  --c-moral:      #4527a0;
  --c-unspecified:#546e7a;
}

body {
  font-family: var(--serif);
  font-size: 1rem;
  line-height: 1.75;
  background: var(--bg);
  color: #1a1612;
  margin: 0;
}

a { color: var(--link); }

/* ── Layout ── */
.page-header {
  background: var(--accent);
  color: #fff;
  padding: 2.5rem 2rem 2rem;
  text-align: center;
}
.page-header h1 { margin: 0 0 .3rem; font-size: 1.8rem; font-weight: 700; }
.page-header .subtitle { font-size: .95rem; opacity: .85; font-family: var(--sans); }

nav#toc {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 1.25rem 2rem;
}
nav#toc h2 {
  font-family: var(--sans);
  font-size: .75rem;
  text-transform: uppercase;
  letter-spacing: .1em;
  color: var(--muted);
  margin: 0 0 .6rem;
}
nav#toc ol {
  margin: 0; padding: 0 0 0 1.2em;
  font-family: var(--sans);
  font-size: .875rem;
  column-count: 2;
  column-gap: 2rem;
}
nav#toc li { margin-bottom: .2rem; }

.container {
  max-width: 820px;
  margin: 0 auto;
  padding: 2rem 1.5rem 4rem;
}

/* ── Sources table ── */
section#sources h2 {
  font-family: var(--sans);
  font-size: 1.05rem;
  font-weight: 600;
  border-bottom: 2px solid var(--accent);
  padding-bottom: .3rem;
  margin-bottom: 1rem;
  color: var(--accent);
}
.source-grid {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: .3rem 1.2rem;
  font-size: .875rem;
  margin-bottom: 2.5rem;
}
.source-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: .8rem 1rem;
  margin-bottom: .6rem;
}
.source-card .source-n {
  display: inline-block;
  background: var(--accent);
  color: #fff;
  font-family: var(--sans);
  font-size: .7rem;
  font-weight: 700;
  border-radius: 3px;
  padding: .05rem .4rem;
  margin-right: .5rem;
}
.source-card .source-name {
  font-weight: 600;
}
.source-card .source-meta {
  font-size: .8rem;
  color: var(--muted);
  font-family: var(--sans);
  margin-top: .25rem;
}
.source-card .source-meta .label {
  font-weight: 600;
  color: #444;
}
.source-card .source-meta a { font-size: .8rem; }

/* ── Div levels ── */
.book {
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 3px solid var(--accent);
}
.book-header {
  margin-bottom: 1.5rem;
}
.book-title {
  font-size: 1.55rem;
  font-weight: 700;
  margin: 0 0 .3rem;
}
.book-badge {
  display: inline-block;
  font-family: var(--sans);
  font-size: .7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .08em;
  padding: .1rem .5rem;
  border-radius: 3px;
  background: #eee;
  color: #555;
}
.book-badge.religious  { background: #f3e5f5; color: #6a1b9a; }
.book-badge.history    { background: #e3f2fd; color: #0d47a1; }
.book-badge.tafsir     { background: #fff8e1; color: #e65100; }
.book-badge.adab       { background: #e8f5e9; color: #1b5e20; }

.section   { margin-left: .5rem; margin-top: 1.5rem; }
.chapter   { margin-left: 1rem;  margin-top: 1.2rem; }
.subchapter{ margin-left: 1.5rem; margin-top: 1rem; }

h2.div-head { font-size: 1.2rem; font-weight: 700; margin: 0 0 .6rem; }
h3.div-head { font-size: 1.05rem; font-weight: 600; margin: 0 0 .5rem; color: #333; }
h4.div-head { font-size: .95rem; font-weight: 600; margin: 0 0 .4rem; color: #444; }
h5.div-head { font-size: .9rem;  font-weight: 600; margin: 0 0 .35rem; color: #555; }

.div-head.r-center { text-align: center; }

/* ── Paragraphs ── */
p.para {
  margin: .6rem 0 .6rem;
}
p.para.r-right,
p.para[data-rend="r-right"] {
  direction: rtl;
  text-align: right;
  font-size: 1.05rem;
}
p.para.ayyat  { background: #fdfaf2; border-left: 3px solid #d4a017; padding: .4rem .8rem; }
p.para.hadith { background: #f5f9ff; border-left: 3px solid #3b6ea5; padding: .4rem .8rem; }

.para-n {
  font-family: var(--sans);
  font-size: .7rem;
  color: var(--muted);
  vertical-align: super;
  margin-right: .25em;
}

/* ── Verse line / milestone ── */
span.lb::before { content: "\A"; white-space: pre; }
span.pb {
  display: inline-block;
  font-family: var(--sans);
  font-size: .65rem;
  color: var(--muted);
  border: 1px solid var(--border);
  border-radius: 2px;
  padding: 0 .25rem;
  margin: 0 .15rem;
  vertical-align: middle;
}

/* ── Inline elements ── */
/* Custom tooltip shared by term, placeName, persName */
span.term,
span.placeName,
span.persName {
  position: relative;
}
span.term[data-tip]::after,
span.placeName[data-tip]::after,
span.persName[data-tip]::after {
  content: attr(data-tip);
  position: absolute;
  bottom: calc(100% + 4px);
  left: 50%;
  transform: translateX(-50%);
  white-space: nowrap;
  background: #1a1612;
  color: #fff;
  font-family: var(--sans);
  font-size: .72rem;
  font-weight: 400;
  font-style: normal;
  padding: .2rem .5rem;
  border-radius: 4px;
  pointer-events: none;
  opacity: 0;
  transition: opacity .15s;
  z-index: 10;
}
span.term[data-tip]:hover::after,
span.placeName[data-tip]:hover::after,
span.persName[data-tip]:hover::after { opacity: 1; }

span.term {
  font-weight: 700;
  padding: .05em .25em;
  border-radius: 3px;
  cursor: help;
}
span.term.natural    { background: #c8e6c9; color: #1b5e20; }
span.term.divine     { background: #e1bee7; color: #4a148c; }
span.term.military   { background: #ffcdd2; color: #b71c1c; }
span.term.political  { background: #ffe0b2; color: #bf360c; }
span.term.social     { background: #bbdefb; color: #0d47a1; }
span.term.moral      { background: #d1c4e9; color: #311b92; }
span.term.unspecified{ background: #cfd8dc; color: #263238; }

span.gloss.translation {
  display: block;
  font-style: italic;
  font-size: .9rem;
  color: #3a3530;
  margin-top: .3rem;
  padding: .2rem .5rem;
  border-left: 2px solid #ccc;
}
span.gloss.arabic-script {
  font-size: 1em;
  direction: rtl;
}
span.gloss.translitteration {
  font-style: italic;
  color: var(--muted);
}

span.persName {
  background: #dce8f5;
  color: #1a3a5c;
  padding: .05em .2em;
  border-radius: 3px;
  font-style: italic;
}
span.placeName {
  background: #d4edda;
  color: #1e5631;
  padding: .05em .2em;
  border-radius: 3px;
  font-weight: 600;
  cursor: help;
}
span.name { font-style: italic; }

span.hi.bold   { font-weight: 700; }
span.hi.italic { font-style: italic; }

/* ── Legend ── */
.legend {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: .8rem 1.2rem;
  margin: 2rem 0 1rem;
  font-family: var(--sans);
  font-size: .8rem;
}
.legend h3 { margin: 0 0 .5rem; font-size: .8rem; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); }
.legend ul { margin: 0; padding: 0; list-style: none; display: flex; flex-wrap: wrap; gap: .4rem .6rem; }
.legend li {
  font-weight: 700;
  padding: .1rem .45rem;
  border-radius: 3px;
  font-size: .78rem;
}
.legend li.natural    { background: #c8e6c9; color: #1b5e20; }
.legend li.divine     { background: #e1bee7; color: #4a148c; }
.legend li.military   { background: #ffcdd2; color: #b71c1c; }
.legend li.political  { background: #ffe0b2; color: #bf360c; }
.legend li.social     { background: #bbdefb; color: #0d47a1; }
.legend li.moral      { background: #d1c4e9; color: #311b92; }
.legend li.unspecified{ background: #cfd8dc; color: #263238; }

/* ── Responsive ── */
@media (max-width: 600px) {
  nav#toc ol { column-count: 1; }
  .book-title { font-size: 1.3rem; }
  p.para.r-right { font-size: 1rem; }
}
        ]]></style>
      </head>
      <body>

        <!-- Page header -->
        <header class="page-header">
          <h1><xsl:value-of select="//tei:titleStmt/tei:title"/></h1>
          <p class="subtitle">
            Edited by <xsl:value-of select="//tei:titleStmt/tei:editor/tei:persName"/>
            &#160;·&#160;
            <xsl:value-of select="//tei:publicationStmt/tei:publisher"/>
            &#160;·&#160;
            <xsl:value-of select="//tei:publicationStmt/tei:date"/>
          </p>
        </header>

        <!-- Table of contents (books) -->
        <nav id="toc">
          <h2>Contents</h2>
          <ol>
            <xsl:for-each select="//tei:body/tei:div1">
              <li>
                <a href="#book{@n}">
                  <xsl:value-of select="tei:head/tei:title"/>
                </a>
              </li>
            </xsl:for-each>
          </ol>
        </nav>

        <div class="container">

          <!-- Sources -->
          <section id="sources">
            <h2>Sources</h2>
            <xsl:apply-templates select="//tei:sourceDesc/tei:msDesc"/>
          </section>

          <!-- Legend -->
          <div class="legend">
            <h3>Disaster term categories</h3>
            <ul>
              <li class="natural">Natural</li>
              <li class="divine">Divine</li>
              <li class="military">Military</li>
              <li class="political">Political</li>
              <li class="social">Social</li>
              <li class="moral">Moral</li>
              <li class="unspecified">Unspecified</li>
            </ul>
          </div>

          <!-- Text body -->
          <xsl:apply-templates select="//tei:body/tei:div1"/>

        </div>
      </body>
    </html>
  </xsl:template>

  <!-- ============================================================ -->
  <!-- SOURCES                                                       -->
  <!-- ============================================================ -->

  <xsl:template match="tei:msDesc">
    <div class="source-card">
      <span class="source-n"><xsl:value-of select="@n"/></span>
      <span class="source-name">
        <xsl:value-of select="tei:msIdentifier/tei:msName"/>
      </span>
      <div class="source-meta">
        <xsl:for-each select="tei:additional/tei:listBibl/tei:bibl">
          <xsl:if test="tei:author">
            <span class="label">Author: </span>
            <xsl:value-of select="tei:author"/>&#160;&#160;
          </xsl:if>
          <xsl:if test="tei:publisher">
            <span class="label">Publisher: </span>
            <xsl:apply-templates select="tei:publisher"/>&#160;&#160;
          </xsl:if>
          <xsl:if test="tei:pubPlace">
            <span class="label">Place: </span>
            <xsl:apply-templates select="tei:pubPlace"/>&#160;&#160;
          </xsl:if>
          <xsl:if test="tei:date">
            <span class="label">Date: </span>
            <xsl:value-of select="tei:date"/>&#160;&#160;
          </xsl:if>
          <xsl:for-each select="tei:ref[@target]">
            <a href="{@target}" target="_blank">
              <xsl:value-of select="."/>
              <xsl:if test="not(normalize-space(.))">
                <xsl:value-of select="@target"/>
              </xsl:if>
            </a>&#160;
          </xsl:for-each>
        </xsl:for-each>
        <xsl:if test="tei:physDesc/tei:objectDesc/tei:p[normalize-space(.)]">
          &#160;(<xsl:apply-templates select="tei:physDesc/tei:objectDesc/tei:p"/>)
        </xsl:if>
      </div>
    </div>
  </xsl:template>

  <!-- ============================================================ -->
  <!-- DIV LEVELS                                                    -->
  <!-- ============================================================ -->

  <xsl:template match="tei:div1">
    <xsl:variable name="cat">
      <xsl:choose>
        <xsl:when test="contains(@ana,'religious')">religious</xsl:when>
        <xsl:when test="@ana='history'">history</xsl:when>
        <xsl:when test="@ana='tafsir'">tafsir</xsl:when>
        <xsl:when test="@ana='adab'">adab</xsl:when>
        <xsl:otherwise>other</xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <div class="book" id="book{@n}">
      <div class="book-header">
        <span class="book-badge {$cat}"><xsl:value-of select="$cat"/></span>
        <xsl:apply-templates select="tei:head" mode="book-title"/>
      </div>
      <xsl:apply-templates select="tei:p | tei:l | tei:lb | tei:pb | tei:byline | tei:div2"/>
    </div>
  </xsl:template>

  <xsl:template match="tei:head" mode="book-title">
    <div class="book-title">
      <xsl:apply-templates/>
    </div>
  </xsl:template>

  <xsl:template match="tei:div2">
    <div class="section">
      <xsl:apply-templates select="tei:head" mode="h2"/>
      <xsl:apply-templates select="tei:p | tei:l | tei:lb | tei:pb | tei:byline | tei:div3"/>
    </div>
  </xsl:template>

  <xsl:template match="tei:div3">
    <div class="chapter">
      <xsl:apply-templates select="tei:head" mode="h3"/>
      <xsl:apply-templates select="tei:p | tei:l | tei:lb | tei:pb | tei:byline | tei:div4"/>
    </div>
  </xsl:template>

  <xsl:template match="tei:div4">
    <div class="subchapter">
      <xsl:apply-templates select="tei:head" mode="h4"/>
      <xsl:apply-templates select="tei:p | tei:l | tei:lb | tei:pb | tei:byline | tei:div5"/>
    </div>
  </xsl:template>

  <xsl:template match="tei:div5">
    <div class="subchapter">
      <xsl:apply-templates select="tei:head" mode="h5"/>
      <xsl:apply-templates select="tei:p | tei:l | tei:lb | tei:pb | tei:byline"/>
    </div>
  </xsl:template>

  <!-- Head elements by level -->
  <xsl:template match="tei:head" mode="h2">
    <xsl:variable name="cls">
      <xsl:text>div-head</xsl:text>
      <xsl:if test="contains(@rendition,'r-center') or contains(@rend,'r-center')"> r-center</xsl:if>
    </xsl:variable>
    <h2 class="{$cls}"><xsl:apply-templates/></h2>
  </xsl:template>

  <xsl:template match="tei:head" mode="h3">
    <xsl:variable name="cls">
      <xsl:text>div-head</xsl:text>
      <xsl:if test="contains(@rendition,'r-center') or contains(@rend,'r-center')"> r-center</xsl:if>
    </xsl:variable>
    <h3 class="{$cls}"><xsl:apply-templates/></h3>
  </xsl:template>

  <xsl:template match="tei:head" mode="h4">
    <xsl:variable name="cls">
      <xsl:text>div-head</xsl:text>
      <xsl:if test="contains(@rendition,'r-center') or contains(@rend,'r-center')"> r-center</xsl:if>
    </xsl:variable>
    <h4 class="{$cls}"><xsl:apply-templates/></h4>
  </xsl:template>

  <xsl:template match="tei:head" mode="h5">
    <xsl:variable name="cls">
      <xsl:text>div-head</xsl:text>
      <xsl:if test="contains(@rendition,'r-center') or contains(@rend,'r-center')"> r-center</xsl:if>
    </xsl:variable>
    <h5 class="{$cls}"><xsl:apply-templates/></h5>
  </xsl:template>

  <!-- Default head fallback (used in mode="book-title" already handled above) -->
  <xsl:template match="tei:head"/>

  <!-- ============================================================ -->
  <!-- BLOCK ELEMENTS                                                -->
  <!-- ============================================================ -->

  <xsl:template match="tei:p">
    <xsl:variable name="cls">
      <xsl:text>para</xsl:text>
      <xsl:choose>
        <xsl:when test="contains(@rend,'r-right') or contains(@rendition,'r-right')"> r-right</xsl:when>
      </xsl:choose>
      <xsl:choose>
        <xsl:when test="@ana='ayyat'"> ayyat</xsl:when>
        <xsl:when test="@ana='hadith'"> hadith</xsl:when>
      </xsl:choose>
    </xsl:variable>
    <p class="{$cls}">
      <xsl:if test="@n and normalize-space(@n)">
        <span class="para-n">(<xsl:value-of select="@n"/>)</span>
      </xsl:if>
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <xsl:template match="tei:l">
    <p class="para">
      <xsl:if test="@n and normalize-space(@n)">
        <span class="para-n"><xsl:value-of select="@n"/>.</span>
      </xsl:if>
      <xsl:apply-templates/>
    </p>
  </xsl:template>

  <xsl:template match="tei:byline">
    <p class="para byline"><em><xsl:apply-templates/></em></p>
  </xsl:template>

  <!-- ============================================================ -->
  <!-- MILESTONES                                                    -->
  <!-- ============================================================ -->

  <xsl:template match="tei:lb">
    <span class="lb"/>
  </xsl:template>

  <xsl:template match="tei:pb">
    <span class="pb">p.<xsl:value-of select="@n"/></span>
  </xsl:template>

  <!-- ============================================================ -->
  <!-- INLINE ELEMENTS                                               -->
  <!-- ============================================================ -->

  <xsl:template match="tei:term">
    <xsl:variable name="subtype">
      <xsl:choose>
        <xsl:when test="contains(@subtype,'natural')">natural</xsl:when>
        <xsl:when test="contains(@subtype,'divine')">divine</xsl:when>
        <xsl:when test="contains(@subtype,'military')">military</xsl:when>
        <xsl:when test="contains(@subtype,'political')">political</xsl:when>
        <xsl:when test="contains(@subtype,'social')">social</xsl:when>
        <xsl:when test="contains(@subtype,'moral')">moral</xsl:when>
        <xsl:otherwise>unspecified</xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <xsl:variable name="tip">
      <xsl:if test="@translation">
        <xsl:value-of select="@translation"/>
      </xsl:if>
      <xsl:if test="@translation and @subtype"> · </xsl:if>
      <xsl:if test="@subtype">
        <xsl:value-of select="@subtype"/>
      </xsl:if>
    </xsl:variable>
    <span class="term {$subtype}">
      <xsl:if test="normalize-space($tip)">
        <xsl:attribute name="data-tip"><xsl:value-of select="$tip"/></xsl:attribute>
      </xsl:if>
      <xsl:apply-templates/>
    </span>
  </xsl:template>

  <xsl:template match="tei:gloss">
    <xsl:variable name="cls">
      <xsl:text>gloss</xsl:text>
      <xsl:choose>
        <xsl:when test="@ana='translation'"> translation</xsl:when>
        <xsl:when test="contains(@ana,'arabic')"> arabic-script</xsl:when>
        <xsl:when test="contains(@ana,'translitteration')"> translitteration</xsl:when>
      </xsl:choose>
      <xsl:if test="@rend='italic'"> italic</xsl:if>
    </xsl:variable>
    <span class="{$cls}"><xsl:apply-templates/></span>
  </xsl:template>

  <xsl:template match="tei:hi">
    <xsl:variable name="cls">
      <xsl:text>hi</xsl:text>
      <xsl:if test="contains(@rendition,'bold') or @rend='bold'"> bold</xsl:if>
      <xsl:if test="@rend='italic'"> italic</xsl:if>
    </xsl:variable>
    <span class="{$cls}"><xsl:apply-templates/></span>
  </xsl:template>

  <xsl:template match="tei:persName">
    <span class="persName">
      <xsl:if test="@translitteration">
        <xsl:attribute name="data-tip"><xsl:value-of select="@translitteration"/></xsl:attribute>
      </xsl:if>
      <xsl:apply-templates/>
    </span>
  </xsl:template>

  <xsl:template match="tei:placeName">
    <span class="placeName">
      <xsl:if test="@translation">
        <xsl:attribute name="data-tip"><xsl:value-of select="@translation"/></xsl:attribute>
      </xsl:if>
      <xsl:apply-templates/>
    </span>
  </xsl:template>

  <xsl:template match="tei:name">
    <span class="name"><xsl:apply-templates/></span>
  </xsl:template>

  <xsl:template match="tei:ref[@target]">
    <a href="{@target}" target="_blank"><xsl:apply-templates/></a>
  </xsl:template>

  <xsl:template match="tei:ref[not(@target)]">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="tei:title">
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="tei:date">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- Suppress header elements outside their expected context -->
  <xsl:template match="tei:teiHeader"/>

</xsl:stylesheet>
