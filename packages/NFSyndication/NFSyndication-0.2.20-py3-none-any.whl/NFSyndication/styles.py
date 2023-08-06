
# -*- coding: utf-8 -*-
import cssutils
# You can decode the cssText in ASCII using the function sheet.cssText.decode('ascii') before writing to CSS file

css = '''
       /* begin */
body {
    font: 12pt Georgia, Palatino, 'Palatino Linotype', Times, 'Times New Roman', serif;
                                        /* font: serif */
    color: #1f501f !important;           /* body-gray */
}

a {
    color: #732c7b;
}

a:hover {
    text-decoration: none;
}

a:visited {
    color: #421c52;
}

hr {
    background-color: #eee;
    height: 1px;
    border: none;
}

hr.between_posts {
    margin-top: 3em;
    margin-bottom: 3em;
}

body {
    margin: 0;
    padding: 0;
}

#header_text {
  padding: 1px 20px 0px 20px;
  color: #eeddf9;
}

#header_text a {
  color: #9aa09a !important;
  text-decoration: none;
}

img {
    margin-left:  auto;
    margin-right: auto;
    display: block;
}

code {
    margin:  2px;
    padding: 2px;
}

code, pre {
    font-family: Menlo, monospace;      /* font: mono */
    background-color: #eee;             /* light-gray */
    font-size: 0.9em;                   /* subfont-size */
}

/**
 * The overflow-x line ensures that extra text only appears within the
 * confines of the gray background, and doesn't spill out onto the page.
 * Effectively the <pre> becomes a 'window' into the code beneath.
 */
pre {
    padding: 10px;
    line-height: 1.35em;
    overflow-x: auto;
}

/*------------------------------------*
  # Footnotes
\*------------------------------------*/

/**
 * The padding-tops adds a little extra space between the bottom of an article
 * and the start of the footnote section.
 */
.footnote {
  font-size: 0.9em;                     /* subfont-size */
}

/**
 * These rules help the positioning of the footnote markers, although I'm not
 * entirely sure how they work.
 */
sup, sub {
  vertical-align: 0ex;
  position: relative;
}

sup { bottom: 1ex; }
sub { top: 0.8ex; }



/*------------------------------------*
  # Article titles
\*------------------------------------*/

.article_title a,
.permalink a,
.continue_reading {
    color: #732c7b !important;          /* primary-red */
}

.fullpost_title a {
    text-decoration: none;
    font-size: 1.5em;
    line-height: 1.5em;
}

/**
 * The article_meta class covers permalinks and posting dates
 */
.article_meta {
    font-size: 0.9em;                   /* subfont-size */
    color: #999;                        /* accent-gray */
}

.linkpost_arrow {
    color: #999;                        /* accent-gray */
}

.permalink a {
    font-size: 1.2em;
    text-decoration: none;
}

/**
 * Adjust the spacing around titles to make them look nice
 */
.linkpost_title {
    margin-bottom: -0.5em;
}

.fullpost_title {
    margin-bottom: -0.3em;
}



/*------------------------------------*
  # Blockquotes
\*------------------------------------*/

blockquote {
    border-left: 5px solid #ccc;        /* primary-red */
    margin-left:  15px;
    margin-right: 0px;
    padding: 1px 15px;
    color: #666;                        /* blockquote-gray */
    font-style: italic;
}

blockquote p {
    margin-top: 10px;
    margin-bottom: 10px;
}



/*------------------------------------*
  # Tweets
\*------------------------------------*/

/**
 * I think Dr. Drang wrote this originally?  Whatever, I have it
 * inlined so that all my CSS comes down in a single file.
 */

.bbpBox {
  width: 80%;
  background: #8ec2da;
  margin-left: auto;
  margin-right: auto;
  padding: 1em;
  margin-top: 1em;
  margin-bottom: 1.1em;
/*  margin: 1em 0em 1.1em 0em;*/
  font-family: Georgia !important;
}

.bbpBox blockquote {
  background-color: white;
  margin: 0em !important;
  padding: .75em .75em .5em .75em !important;
  -moz-border-radius: 5px;
  -webkit-border-radius: 5px;
  border-left-style: none !important;
  font-style: normal !important;
  line-height: 1.5em;
  color: #222;
}

.bbpBox blockquote a {
  color: blue;
  text-decoration: none;
}

.bbpBox blockquote a:hover {
  text-decoration: underline;
}

.bbpBox blockquote .twMeta {
  font-size: 80%;
}

.bbpBox blockquote .twContent {
  margin-bottom: 25em;
}

body {
  background-color: #140623;
  max-width: 750px;
  margin-top: 0;
  margin-left: auto;
  margin-right: auto;
  padding-top: 0;
}

h1 {
  font-size: 2.5em;
}

.rss {
  list-style-type: none;
  margin: 0;
  padding: .5em 1em 1em 1.5em;
  background-color: white;
  margin-bottom: 2em;
}

.rss li {
  margin-left: -.5em;
  line-height: 1.4;
}

.rss li pre {
  overflow: auto;
}

img, figure, iframe {
  max-width: 700px;
  height: auto !important;
}

@media screen and (max-width: 700px) {
  img, figure, iframe {
    max-width: 100% !important;
  }
}


.footnotes {
    font-size: 0.85em;
}

a code {
    text-decoration: none !important;
}

footer {
  color: #eeddf9;
  text-align: center;
  margin-bottom: 2.2em;
  font-size: 0.85em;
}

footer a {
  color: #eeddf9 !important;
} /* end */
''';

sheet = cssutils.parseString(css)

for rule in sheet:
    if rule.type == rule.STYLE_RULE:
        # find property
        for property in rule.style:
            if property.name == 'color':
                property.value = 'green'
                property.priority = 'IMPORTANT'
                break
        # or simply:
        # rule.style['margin'] = '01.0eM' # or: ('1em', 'important')  
        
        # Remind: rule.style['margin'] is not necessary.


# cssutils.ser.prefs.resolveVariables == True since 0.9.7b2
cssTextDecoded = sheet.cssText.decode('ascii')
#print(cssTextDecoded)
with open("output/style.css", 'w') as f:
    f.write(cssTextDecoded)
