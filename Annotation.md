# DiCCAS XML Annotation Guide (Compact)

- [DiCCAS XML Annotation Guide (Compact)](#diccas-xml-annotation-guide-compact)
  - [XML STRUCTURE](#xml-structure)
  - [STRUCTURE TAGS](#structure-tags)
  - [ANNOTATION TAGS](#annotation-tags)

This guide describes the XML tags used in the DiCCAS Disaster Corpus for
textual annotation. Root and metadata sections (TEI, teiHeader, etc.)
are excluded.

## XML STRUCTURE

```
text
 └── body
      └── div
           └── div1
                └── p
                     ├── term
                     │    └── hi
                     ├── gloss
                     ├── placename
                     │    └── hi
                     └── lb
```

## STRUCTURE TAGS

1. `<text/>`: Container for the encoded text. Subtags: `body`
  Example:

    ```xml
    <text>
      <body>...</body>
    </text>
    ```

2. `<body/>`: Contains the main corpus content. Subtags: `div`, `div1`, `p`
   Example:

    ```xml
    <body>
      <div type="book" ana="religious" n="1">
      </div>
    </body>
    ```

3. `<div/>`: Major structural section (e.g., book). Subtags: `head`, `div1`, `p`
  Example:

    ```xml
    <div type="book" ana="religious" n="1">
      <head>كتاب التفسير</head>
    </div>
    ```

    | Attribute | Description         | Values                            |
    | --------- | ------------------- | --------------------------------- |
    | `type`    | division type       | book                              |
    | `ana`     | analytical category | religious, history, tafsir, adab, |
    | `n`       | book number         | 1 to 10                           |

4. `<divX/>`: Subdivision of a division (e.g., sura or chapter).
  Example:

    ```xml
    <div1 type="sura" n="2">
      <head>سورة البقرة</head>
    </div1>
    ```

   | Attribute | Description     | Values                                            |
   | --------- | --------------- | ------------------------------------------------- |
   | `type`    | subsection type | section, sura, chapter, subchapter, subsubchapter |
   | `n`       | identifier      |                                                   |

5. `<head/>`: Section title.
   Example:

    ```xml
    <head type="subtitle">سورة البقرة</head>
    ```

   | Attribute   | Description  | Values              |
   | ----------- | ------------ | ------------------- |
   | `type`      | heading type | title, subtitle etc |
   | `rendition` | formatting   |                     |

6. `<p/>`: Paragraph or verse unit. Subtags: `term`, `hi`, `gloss`, `placename`
  Example:

    ```xml
    <p id="423" rend="#normal" n="" type="paragraph">
        <pb n="292"/>وحج في هذه السنة الملك الناصر حسن بن أبي بكر بن حسن بن بدر الدين متملك ديوة - التي تسميها العامة دينة وهي جزائر في البحر تجاور<term type="catastrophe" translation="flood"><hi rendition="bold">‌سيلان </hi></term>. وفيها وقع <term type="catastrophe"   translation="pestilence"> <hi rendition="bold">وَبَاء </hi></term> عظيم ببلاد كرمان. وأبتدأ في مدينة هراة من بلاد<placename translation="Khorasan"><hi rendition="bold">خراسان</hi></placename> في شهر ربيع الأول وشنع فمات فيه عالم عظيم يقول المكثر ثمانمائة ألف.
    </p>
    ```

   | Attribute | Description          | Value                      |
   | --------- | -------------------- | -------------------------- |
   | `id`      | paragraph identifier | corpus specific identifier |
   | `n`       | verse number         |                            |
   | `ana`     | annotation category  | ayyat                      |
   | `rend`    | text alignment       |                            |
   | `note`    | additional note      |                            |

## ANNOTATION TAGS

1. `<term/>`: Marks disaster-related concepts.
   Example:

    ```xml
    <term type="catastrophe" translation="hunger">
      <hi rendition="bold">والجوع</hi>
    </term>
    ```

   | Attribute     | Description         | Value       |
   | ------------- | ------------------- | ----------- |
   | `type`        | category            | catastrophe |
   | `subtype`     | subcategory         | divine, natural, unspecified, military, social, political |
   | `translation` | English translation |             |

2. `<hi/>`: Highlighted text.
  Example:

    ```xml
    <hi rendition="bold">مصيبة</hi>
    ```

   | Attribute   | Description      |
   | ----------- | ---------------- |
   | `rendition` | formatting style |

3. `<gloss/>`: Translation or explanatory note.

   | Attribute  | Description     |
   | ---------- | --------------- |
   | `ana`      | annotation type |
   | `rend`     | text style      |
   | `xml:lang` | language        |

4. `<placename/>`: Geographical location.
   Example:

    ```xml
    <placename translation="Cairo">
      <hi rendition="bold">القاهرة</hi>
    </placename>
    ```

   | Attribute     | Description        |
   | ------------- | ------------------ |
   | `translation` | English place name |
