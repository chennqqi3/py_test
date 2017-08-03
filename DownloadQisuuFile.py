#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
==Function==
DownloadQisuuFile - 下载奇书网(qisuu.com)的电子书文件
http://www.crifan.com/crifan_released_all/website/python/downloadqisuufile/

==Version==
[v1.0 - 2012-12-17]
1.initial version

-------------------------------------------------------------------------------
"""
#--------------------------------const values-----------------------------------
__VERSION__ = "v1.0";

gConst = {

};

gCfg = {
    'downloadFolder'    : None,
};

gVal = {
    'mainPreUrl'    : None,
};

#---------------------------------import---------------------------------------
import os;
import re;
import sys;
sys.path.append("libs");
from BeautifulSoup import BeautifulSoup,Tag,CData;
import crifanLib;
import logging;
import argparse;

# import urllib;
# import json;
# import csv;
# import codecs;

def main():
    logging.info("Version: %s", __VERSION__);

    newParser = argparse.ArgumentParser(description="Download (ebook) file from qisuu");
    newParser.add_argument("-s", "--startTypeUrl", dest="startTypeUrl", help="start url of type. eg: http://www.qisuu.com/soft/sort03/sort039/list39_1.html, http://www.qisuu.com/soft/sort02/list2_1.html");
    newParser.add_argument("-n", "--startPageNum", dest="startPageNum", type=int, default=1, help="start page number");
    newParser.add_argument("-d", "--downloadFolder", dest="downloadFolder", default="download", help="foler name to store downloaded files");
    args = newParser.parse_args();
    argsDict = args.__dict__;
    for eachArg in argsDict.keys():
        exec(eachArg + " = args." + eachArg);
 
    logging.info("startTypeUrl=%s", startTypeUrl);
    logging.info("startPageNum=%d", startPageNum);
    logging.info("downloadFolder=%s", downloadFolder);

    gConst['downloadFolder'] = downloadFolder;

    foundMainPrefUrl = re.search("(?P<mainPreUrl>http://www\.qisuu\.com/[\w/]+/list\d+_)\d+.html", startTypeUrl);
    logging.debug("foundMainPrefUrl=%s", foundMainPrefUrl);
    if(foundMainPrefUrl):
        mainPreUrl = foundMainPrefUrl.group("mainPreUrl");
        logging.info("mainPreUrl=%s", mainPreUrl);
        gVal['mainPreUrl'] = mainPreUrl;
    else:
        logging.error("Can Not found main prefix url from %s", startTypeUrl);
        sys.exit(-1);

    #init
    if(os.path.isdir(gConst['downloadFolder']) == False):
        os.makedirs(gConst['downloadFolder']);# create dir recursively
 
    #extract total page number
    respHtml = crifanLib.getUrlRespHtml(startTypeUrl);
    #logging.debug("respHtml=%s", respHtml);
    respHtmlUni = respHtml.decode("GBK", 'ignore');
    #       <td class="tablebody1">&nbsp;<a href="list39_72.html" title="尾页"><img border="0" src="/images/Last.gif" /></a>&nbsp;</td>
    foundTotalPageNum = re.search(u'<a\s+href="list\d+_(?P<totalPageNum>\d+).html"\s+title="尾页">', respHtmlUni);
    logging.debug("foundTotalPageNum=%s", foundTotalPageNum);
    if(foundTotalPageNum):
        totalPageNum = foundTotalPageNum.group("totalPageNum");
        logging.info("totalPageNum=%s", totalPageNum);
        totalPageNum = int(totalPageNum);
    else:
        logging.error("Can Not found total page number from %s resp html:\n%s", startTypeUrl, respHtml);
        sys.exit(-2);

    #for num in range(1, totalPageNum+1):
    for pageNum in range(startPageNum, totalPageNum+1):
        logging.info("============== page=%d ==============", pageNum);
        #http://www.qisuu.com/soft/sort03/sort039/list39_1.html
        #eachPageUrl = "http://www.qisuu.com/soft/sort03/sort039/list39_"+str(pageNum)+".html";
        eachPageUrl = gVal['mainPreUrl'] + str(pageNum) + ".html";
        logging.info("eachPageUrl=%s", eachPageUrl);
        pageRespHtml = crifanLib.getUrlRespHtml(eachPageUrl);
        #logging.debug("pageRespHtml=%s", pageRespHtml);
        # <div class="mainListInfo">
            # <div class="mainListName"><span class="mainSoftName"><a href="/Shtml27341.html" title="《所遇非淑》全集">《所遇非淑》全集</a></span></div><div class="mainListSize">2.06 MB</div><div class="mainListDate"><span class="oldDate"><span class="oldDate">2012-12-16</span></span></div><div class="mainListHist">Jar+TXT版</div>
        # </div>
        soup = BeautifulSoup(pageRespHtml, fromEncoding="GBK");
        foundAllMainList = soup.findAll(name="span", attrs={"class":"mainSoftName"});
        logging.debug("foundAllMainList=%s", foundAllMainList);
        mainListLen = len(foundAllMainList);
        logging.info("mainListLen=%s", mainListLen);
        for urlIdx,eachMainList in enumerate(foundAllMainList):
            urlNum = urlIdx + 1;
            logging.info("-------------- page=%d, url=%d --------------", pageNum, urlNum);
            logging.debug("eachMainList=%s", eachMainList);
            href = eachMainList.a['href'];
            logging.debug("href=%s", href);
            #http://www.qisuu.com/Shtml27667.html
            eachFileUrl = "http://www.qisuu.com" + href;
             
            logging.info("eachFileUrl=%s", eachFileUrl);
            fileRespHtml = crifanLib.getUrlRespHtml(eachFileUrl);
            #logging.debug("fileRespHtml=%s", fileRespHtml);
            soup = BeautifulSoup(fileRespHtml, fromEncoding="GBK");
             
            h1 = soup.h1.string;
            logging.info("h1=%s", h1);
            ebooName = h1 + ".rar";
             
            # <img src="/skin/newasp/download.gif"> <A oncontextmenu=ThunderNetwork_SetHref(this) onclick='return OnDownloadClick_Simple(this,2)' href='#' thunderResTitle='http://dzs.qisuu.com/2013012903.rar' thunderType='' thunderPid='02503' thunderHref='thunder://QUFodHRwOi8vZHpzLnFpc3V1LmNvbS8yMDEzMDEyOTAzLnJhclpa'class=downLinks>迅雷专用高速下载点</A><br><img src=/skin/newasp/download.gif> <A  href='http://dzs.qisuu.com/2013012903.rar'><strong>本站下载地址</strong></A>
            # </div></div>
            #foundEbookAddress = re.search("thunderResTitle='(?P<ebookAddress>http://dzs\.qisuu\.com/\d+\.rar)'", fileRespHtml);
             
            #http://www.qisuu.com/Shtml22388.html
            #http://dzs.qisuu.com/tiansyiduity.rar
            #foundEbookAddress = re.search("thunderResTitle='(?P<ebookAddress>http://dzs\.qisuu\.com/\w+\.rar)'", fileRespHtml);
             
            #http://www.qisuu.com/Shtml23411.html
            #<img src="/skin/newasp/download.gif"> <A oncontextmenu=ThunderNetwork_SetHref(this) onclick='return OnDownloadClick_Simple(this,2)' href='#' thunderResTitle='/soft/download.asp?softid=23411&downid=0&id=67531' thunderType='' thunderPid='02503' thunderHref='thunder://QUEvc29mdC9kb3dubG9hZC5hc3A/c29mdGlkPTIzNDExJmRvd25pZD0wJmlkPTY3NTMxWlo='class=downLinks>迅雷专用高速下载点</A><br><img src=/skin/newasp/download.gif> <A  href='/soft/download.asp?softid=23411&downid=0&id=67531'><strong>本站下载地址</strong></A>
            foundEbookAddress = re.search("thunderResTitle='(?P<ebookAddress>[^']+)'", fileRespHtml);
             
            logging.debug("foundEbookAddress=%s", foundEbookAddress);
             
            if(foundEbookAddress):
                #http://dzs.qisuu.com/2013012903.rar
                #http://dzs.qisuu.com/tiansyiduity.rar
                ebookAddress = foundEbookAddress.group("ebookAddress");
                logging.info("ebookAddress=%s", ebookAddress);
                 
                if(re.match("/soft/download\.asp\?", ebookAddress)):
                    #find out real ebook address
                    #http://www.qisuu.com/Shtml23411.html
                    #->
                    #http://www.qisuu.com/soft/download.asp?softid=23411&downid=0&id=67531
                    #it allow download
                    #actually it will auto direct to:
                    #http://dl.wrshu.com:111/moqiqxdxz.rar
                    downloadAddress = "http://www.qisuu.com" + ebookAddress;
                    logging.info("downloadAddress=%s", downloadAddress);
                    fixedEbookAddress = downloadAddress;
                    logging.info("Found partial ebook address, so fix it to: %s", fixedEbookAddress);
                elif(re.match("http://dzs\.qisuu\.com/", ebookAddress)):
                    fixedEbookAddress = ebookAddress;
                else:
                    logging.error("Can Not recognize this kind of ebook download address %s", ebookAddress);
                    logging.debug("fileRespHtml=%s", fileRespHtml);
                    continue;
 
                #for
                #http://www.qisuu.com/Shtml26634.html
                #title is: 《神魔手下好当差/穿越之傀儡娃娃》全集
                ebookFullName = os.path.join(gConst['downloadFolder'], crifanLib.removeInvalidCharInFilename(ebooName, '_'));
                logging.info("dowloadinging ebookFullName=%s", ebookFullName);
                crifanLib.downloadFile(fixedEbookAddress, ebookFullName, True);
                #crifanLib.downloadFile(fixedEbookAddress, ebookFullName);
            else:
                logging.warning("Not found ebook address for url=%s", eachFileUrl);
                logging.debug("record its fileRespHtml=\n%s", fileRespHtml);
                 
                if(foundEbookAddress == None):
                    #http://www.qisuu.com/Shtml23542.html
                    logging.info(u"this url=%s may be: 此电子书已删除，暂不提供下载", eachFileUrl);

###############################################################################
if __name__=="__main__":
    scriptSelfName = crifanLib.extractFilename(sys.argv[0]);
 
    logging.basicConfig(
                    level    = logging.DEBUG,
                    format   = 'LINE %(lineno)-4d  %(levelname)-8s %(message)s',
                    datefmt  = '%m-%d %H:%M',
                    filename = scriptSelfName + ".log",
                    filemode = 'w');
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler();
    console.setLevel(logging.INFO);
    # set a format which is simpler for console use
    formatter = logging.Formatter('LINE %(lineno)-4d : %(levelname)-8s %(message)s');
    # tell the handler to use this format
    console.setFormatter(formatter);
    logging.getLogger('').addHandler(console);
    try:
        main();
    except:
        logging.exception("Unknown Error !");
        raise;