<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0">

    <xsl:template match="/">
        <html>
            <head>
                <title><xsl:value-of select=".//tei:titleStmt/tei:title"/></title>
            </head>
            <body>
                <h1>A Wolf Lying in Wait</h1>
                <div><p>Selected Poems by Abbas Kiarostami</p></div>
                <h2>Introduction</h2>
                    <div>
                        <p>These selected poems are published by Sokhan publication in a bilingual edition in 2005. We have selected 15 poems of the book and annotated it in TEI format.</p>
                    </div>
                <div>
                    <p>Digital Edition by:
                    Nazanin Fakharian
                    Zahra Faraji
                    Ahmadreza Nazari</p>
                </div>
                <h2>Selected Poems</h2>
                <xsl:for-each select=".//tei:body/tei:div">
                    <xsl:choose>
                        <xsl:when test="@type='translation of poem'">
                            <h3>(<xsl:value-of select="@n"/>)</h3>
                            <xsl:for-each select="tei:lg/tei:l">
                                <p><xsl:value-of select="."/></p>
                            </xsl:for-each>
                        </xsl:when>

                        <xsl:when test="@type='original poem'">
                            <h3>(<xsl:value-of select="@n"/>)</h3>
                            <xsl:for-each select="tei:lg/tei:l">    
                                <p><xsl:value-of select="."/></p>
                            </xsl:for-each>
                        </xsl:when>                        
                    </xsl:choose>
                </xsl:for-each>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>