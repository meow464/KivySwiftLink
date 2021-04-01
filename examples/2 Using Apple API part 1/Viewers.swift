//
//  WebViewer.swift
//  kivy_swifttest
//
//  Created by macdaw on 01/04/2021.
//

import Foundation
import UIKit
import WebKit
import PDFKit



class WebViewer: UIViewController,WKNavigationDelegate {
    var webview: WKWebView!
    
    override func loadView() {
        webview = WKWebView()
        webview.navigationDelegate = self
        view = webview
    }
    
    func loadURL(path: String) {
        
        let url = URL(string: path)!
        print(url)
        webview.load(URLRequest(url: url))
    }
}


class PDF_Viewer: UIViewController {
    
    let pdfView = PDFView()
    
    override func loadView() {
        //pdfView = PDFView.init()
        self.view = pdfView
    }
    
    func loadPDF(path: String) {
        let filepath = "YourApp/".appending(path)
        let url = resourceUrl(forFileName: filepath)!
        let doc = PDFDocument(url: url)
        print(doc as Any)
        self.pdfView.document = doc
        
        
    }
    
    private func resourceUrl(forFileName fileName: String) -> URL? {
        if let resourceUrl = Bundle.main.url(forResource: fileName,
                                             withExtension: "pdf") {
            return resourceUrl
        }
        print("url error")
        return nil
    }
    
}
