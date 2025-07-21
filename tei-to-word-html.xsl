<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="tei">
    
    
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>
    
    <!-- Default copy template -->
    <xsl:template match="processing-instruction()">
        <xsl:copy>
            <xsl:apply-templates select="@* | node()"/>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>
    
    <!-- Paragraphs -->
    <xsl:template match="tei:p">
        <p>
            <xsl:apply-templates/>
        </p>
    </xsl:template>
    
    <!-- Titles -->
    <xsl:template match="tei:title">
        <h2>
            <xsl:apply-templates/>
        </h2>
    </xsl:template>
    
    <!-- Headings -->
    <xsl:template match="tei:head">
        <h3>
            <xsl:apply-templates/>
        </h3>
    </xsl:template>
    
    <!-- Gloss in italic -->
    <xsl:template match="tei:gloss">
        <i>
            <xsl:apply-templates/>
        </i>
    </xsl:template>
    
    <!-- Term -->
    <xsl:template match="tei:term">
        <span style="color:darkred;">
            <xsl:apply-templates/>
        </span>
    </xsl:template>
    
    <!-- <hi rendition="..."> mapped to style -->
    <xsl:template match="tei:hi">
        <xsl:choose>
            <xsl:when test="@rendition='bold'">
                <b><xsl:apply-templates/></b>
            </xsl:when>
            <xsl:when test="@rendition='italic'">
                <i><xsl:apply-templates/></i>
            </xsl:when>
            <xsl:when test="@rendition='underline'">
                <u><xsl:apply-templates/></u>
            </xsl:when>
            <xsl:otherwise>
                <span><xsl:apply-templates/></span>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <!-- Line break -->
    <xsl:template match="tei:lb">
        <br/>
    </xsl:template>
    
</xsl:stylesheet>

