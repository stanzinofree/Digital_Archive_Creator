<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method='html' version='2.0' encoding='UTF-8' indent='yes'/>

    <!-- Nodo Principale del file XML REQUEST-->
    <xsl:template match="/">
        <html>
            <body>
                <xsl:for-each select="REQUEST">
                    <p align="center">
                        <h1>Dispositivo Sezione Telematica:
                            <xsl:value-of select="substring(DEVICEID,1,7)"/>
                        </h1>
                    </p>
                    <!--<h1>Report del:<xsl:text> </xsl:text>
                    <xsl:value-of select="substring(DEVICEID,17,2)"/>
                    <xsl:text>/</xsl:text>
                    <xsl:value-of select="substring(DEVICEID,14,2)"/>
                    <xsl:text>/</xsl:text>
                    <xsl:value-of select="substring(DEVICEID,9,4)"/>
                    </h1>
                    -->
                </xsl:for-each>
                <table>
                    <tr>
                        <td valign="top">
                            <table border="1">
                                <tr bgcolor="#9acd32">
                                    <th align="left">Marca</th>
                                    <th align="left">Modello</th>
                                    <th align="left">Versione</th>
                                </tr>
                                <xsl:for-each select="REQUEST/CONTENT/BIOS">
                                    <tr>
                                        <td>
                                            <xsl:value-of select="SMANUFACTURER"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="SMODEL"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="BVERSION"/>
                                        </td>
                                    </tr>
                                </xsl:for-each>
                            </table>
                        </td>
                        <td valign="top">
                            <table border="1">
                                <tr bgcolor="#9acd32">
                                    <th align="left">MONITOR</th>
                                    <th align="left">DESCRIZIONE</th>
                                    <th align="left">SERIALE</th>
                                </tr>
                                <xsl:for-each select="REQUEST/CONTENT/MONITORS">
                                    <tr>
                                        <td>
                                            <xsl:value-of select="MANUFACTURER"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="DESCRIPTION"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="SERIAL"/>
                                        </td>
                                    </tr>
                                </xsl:for-each>
                            </table>
                        </td>
                    </tr>
                </table>
                <table>
                    <tr>
                        <td valign="top">
                            <table border="1">
                                <tr bgcolor="#9acd32">
                                    <th align="left">PROCESSORE</th>
                                    <th align="left">SISTEMA OPERATIVO</th>
                                    <th align="left">SERVICE PACK</th>
                                    <th align="left">UTENTE LOGGATO</th>
                                </tr>
                                <xsl:for-each select="REQUEST/CONTENT/HARDWARE">
                                    <tr>
                                        <td>
                                            <xsl:value-of select="PROCESSORT"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="OSNAME"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="OSCOMMENTS"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="USERID"/>
                                        </td>
                                    </tr>
                                </xsl:for-each>
                            </table>
                        </td>
                    </tr>
                </table>
                <table>
                    <tr>
                        <td valign="top">
                            <table border="1">
                                <tr bgcolor="#9acd32">
                                    <th align="left">KEY SISTEMA OPERATIVO</th>
                                    <th align="left">CODICE SERIALE</th>
                                </tr>
                                <xsl:for-each select="REQUEST/CONTENT/HARDWARE">
                                    <tr>
                                        <td>
                                            <xsl:value-of select="WINPRODKEY"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="WINPRODID"/>
                                        </td>
                                    </tr>
                                </xsl:for-each>
                            </table>
                        </td>
                    </tr>
                </table>
                <p>
                </p>
                <table>
                    <tr>
                        <td valign="top">
                            <table border="1">
                                <tr bgcolor="#9acd32">
                                    <th align="left">MEMORIA MB</th>
                                    <th align="left">TIPO</th>
                                    <th align="left">MHZ</th>
                                </tr>
                                <xsl:for-each select="REQUEST/CONTENT/MEMORIES">
                                    <tr>
                                        <xsl:if test="CAPACITY &gt; 0">
                                            <td>
                                                <xsl:value-of select="CAPACITY"/>
                                            </td>
                                            <td>
                                                <xsl:value-of select="TYPE"/>
                                            </td>
                                            <td>
                                                <xsl:value-of select="SPEED"/>
                                            </td>
                                        </xsl:if>
                                    </tr>
                                </xsl:for-each>
                            </table>
                        </td>
                        <td valign="top">
                            <table border="1">
                                <tr bgcolor="#9acd32">
                                    <th align="left">Disco</th>
                                    <th align="left">Totale MB</th>
                                    <th align="left">Libero MB</th>
                                </tr>
                                <xsl:for-each select="REQUEST/CONTENT/DRIVES">
                                    <tr>
                                        <xsl:if test="TOTAL &gt; 0">
                                            <td>
                                                <xsl:value-of select="LETTER"/>
                                            </td>
                                            <td>
                                                <xsl:value-of select="TOTAL"/>
                                            </td>
                                            <td>
                                                <xsl:value-of select="FREE"/>
                                            </td>
                                        </xsl:if>
                                    </tr>
                                </xsl:for-each>
                            </table>
                        </td>
                        <td valign="top">
                            <table border="1">
                                <tr bgcolor="#9acd32">
                                    <th align="left">Unita'</th>
                                    <th align="left">Tipo</th>
                                </tr>
                                <xsl:for-each select="REQUEST/CONTENT/DRIVES">
                                    <tr>
                                        <td>
                                            <xsl:value-of select="LETTER"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="TYPE"/>
                                        </td>
                                    </tr>
                                </xsl:for-each>
                            </table>
                        </td>
                    </tr>
                </table>
                <p>
                </p>
                <table>
                    <tr>
                        <td>
                            <table border="1">
                                <tr bgcolor="#9acd32">
                                    <th align="left">STAMPANTI</th>
                                    <th align="left">DRIVER</th>
                                    <th align="left">PORTA</th>
                                </tr>
                                <xsl:for-each select="REQUEST/CONTENT/PRINTERS">
                                    <tr>
                                        <td>
                                            <xsl:value-of select="NAME"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="DRIVER"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="PORT"/>
                                        </td>
                                    </tr>
                                </xsl:for-each>
                            </table>
                        </td>
                        <td>
                            <table border="1">
                                <tr bgcolor="#9acd32">
                                    <th align="left">SLOT PCI</th>
                                    <th align="left">DESCRIZIONE</th>
                                </tr>
                                <xsl:for-each select="REQUEST/CONTENT/SLOTS">
                                    <tr>
                                        <!--<xsl:if test = "contains(NAME, 'PCI')">-->
                                        <td>
                                            <xsl:value-of
                                                    select="count(//SLOTS[position()=2 and contains(NAME,'PCI')])"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="DESIGNATION"/>
                                        </td>
                                        <!--		<td><xsl:value-of select="count(//SLOTS[position()=2 and contains(@NAME,'PCI')])"/></td>-->
                                        <!--		<td><xsl:value-of select="count(//SLOTS[NAME='PCI1'])"/></td>-->
                                        <!--</xsl:if>-->
                                    </tr>
                                </xsl:for-each>
                            </table>
                        </td>
                    </tr>
                </table>
                <p>
                </p>
                <table>
                    <tr>
                        <td valign="top">
                            <table border="1">
                                <tr bgcolor="#9acd32">
                                    <th align="left">SCHEDE DI RETE</th>
                                    <th align="left">TIPO</th>
                                    <th align="left">VELOCITA'</th>
                                    <th align="left">MAC ADDRESS</th>
                                    <th align="left">IP</th>
                                    <th align="left">SOTTORETE</th>
                                </tr>
                                <xsl:for-each select="REQUEST/CONTENT/NETWORKS">
                                    <tr>
                                        <td>
                                            <xsl:value-of select="DESCRIPTION"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="TYPE"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="SPEED"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="MACADDR"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="IPADDRESS"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="IPSUBNET"/>
                                        </td>
                                    </tr>
                                </xsl:for-each>
                            </table>
                        </td>
                    </tr>
                </table>
                <p>
                </p>
                Porte presenti sul Dispositivo
                <table>
                    <tr>
                        <td valign="top">
                            <table border="1">
                                <tr bgcolor="#9acd32">
                                    <th align="left">SATA</th>
                                    <th align="left">USB</th>
                                    <th align="left">TASTIERA</th>
                                    <th align="left">MOUSE</th>
                                    <th align="left">AUDIO</th>
                                    <th align="left">VIDEO</th>
                                    <th align="left">RETE</th>
                                    <th align="left">SERIALE</th>
                                    <th align="left">PARALLELA</th>
                                    <th align="left">LETTORE DI SCHEDE</th>
                                    <th align="left">FLOPPY</th>
                                </tr>
                                <xsl:for-each select="REQUEST/CONTENT">
                                    <tr>
                                        <td>
                                            <xsl:value-of select="count(//PORTS[TYPE='SATA'])"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="count(//PORTS[TYPE='USB'])"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="count(//PORTS[TYPE='Keyboard Port'])"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="count(//PORTS[TYPE='Mouse Port'])"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="count(//PORTS[TYPE='Audio Port'])"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="count(//PORTS[TYPE='Video Port'])"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="count(//PORTS[TYPE='Network Port'])"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="count(//PORTS[NAME='COM A'])"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="count(//PORTS[NAME='PARALLEL'])"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select="count(//PORTS[NAME='MEDIA CARD'])"/>
                                        </td>
                                        <xsl:choose>
                                            <xsl:when test="PORTS/NAME = 'FLOPPY' and PORTS/TYPE = 'None'">
                                                <td>-----</td>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <td>
                                                    <xsl:value-of select="count(PORTS[NAME='FLOPPY'])"/>
                                                </td>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </tr>
                                </xsl:for-each>
                            </table>
                        </td>
                    </tr>
                </table>
                <p>
                </p>
                <p style="page-break-before: always"/>
                SOFTWARE INSTALLATO SUL DISPOSITIVO
                <table>
                    <tr>
                        <td valign="top">
                            <table border="1">
                                <tr bgcolor="#9acd32">
                                    <th align="left">DESCRIZIONE</th>
                                    <th align="left">VERSIONE</th>
                                </tr>
                                <xsl:for-each select="REQUEST/CONTENT/SOFTWARES/NAME[not(.=preceding::NAME)]">

                                    <xsl:sort select="../NAME"/>

                                    <xsl:if test="not(contains(../NAME, 'Update')) and not(contains(../NAME, 'Hotfix')) and not(contains(../NAME, 'Security')) and not(contains(../NAME, 'Aggiornamento')) and not(contains(../NAME, 'Language')) and not(contains(../NAME, 'Proof')) and not(contains(../NAME, '{')) and not(contains(../NAME, '(')) and not(contains(../NAME, 'KB')) and not(contains(../NAME, 'MUI')) and not(contains(../NAME, 'Prof')) and not(contains(../NAME, 'VMware'))">
                                        <tr>

                                            <td>
                                                <xsl:value-of select="."/>
                                            </td>
                                            <td>
                                                <xsl:value-of select="../VERSION"/>
                                            </td>
                                        </tr>

                                    </xsl:if>
                                </xsl:for-each>

                                <!-- 		<xsl:attribute name="style">
                                                <xsl:choose>
                                                <xsl:when test="position() mod 2 = 0">
                                                    background-color:silver;
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    background-color:#9acd32;
                                                </xsl:otherwise>
                                                </xsl:choose>
                                        </xsl:attribute>
                                        <xsl:if test="(position() mod 2 = 1)">
                                            <xsl:attribute name="bgcolor">#9acd32</xsl:attribute>
                                        </xsl:if>
                                        -->

                            </table>
                        </td>
                    </tr>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
