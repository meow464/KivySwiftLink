//
//  PythonMain.swift
//  kivy_swifttest
//
//  Created by macdaw on 30/03/2021.
//

import Foundation
import UIKit
import WebKit


class PythonMain : NSObject {
    
    var callback: KivyTestCallback?
    var apple_callback: AppleApiCallback?
    var viewcontroller: UIViewController?
    var web_viewer: WebViewer
    var pdf_viewer: PDF_Viewer
    
    static let shared = PythonMain()
    
    private override init() {
        web_viewer = WebViewer()
        pdf_viewer = PDF_Viewer()
        super.init()
        InitKivyTestDelegate(self) //sets the cython/objc wrapper class delegate target
        InitAppleApiDelegate(self)
        
        
        
    }
}

extension PythonMain: WKNavigationDelegate {
    
}


extension PythonMain : KivyTestDelegate {
    func set_KivyTest_Callback(_ callback: KivyTestCallback) {
        self.callback = callback
        
        self.viewcontroller = self.get_viewcontroller()
    }
    
    func send_python_list(_ l: UnsafePointer<Int32>, l_size: Int) {
        let array = pointer2array(data: l, count: l_size)
        print("python list: ", array)

        callback!.get_swift_array(array.reversed(), array.count)
    }
    
    func send_python_string(_ s: UnsafePointer<Int8>) {
        let string = String.init(cString: s)
        print(string)
                
        let swift_string = "Hallo from swift !!!!"
        callback!.get_swift_string(swift_string)
    }
    
}

extension PythonMain : AppleApiDelegate {
    func set_AppleApi_Callback(_ callback: AppleApiCallback) {
        self.apple_callback = callback
        self.viewcontroller = get_viewcontroller()
    }
    
    func open_files() {
        let documentPicker = UIDocumentPickerViewController(documentTypes: [], in: .open)
        showPopup(view: documentPicker)
    }
    
    func open_pdf(_ path: UnsafePointer<Int8>) {
        showPopup(view: pdf_viewer)
        pdf_viewer.loadPDF(path: path.asString())
    }
    
    func open_web_view(_ path: UnsafePointer<Int8>) {
        showPopup(view: web_viewer)
        web_viewer.loadURL(path: path.asString())
        
        
    }
    
    func showPopup(view: UIViewController) {
        guard let controller = get_viewcontroller() else {return}
        controller.present(view, animated: true, completion: nil)
    }
    
    func get_viewcontroller() -> UIViewController? {
        let window = UIApplication.shared.windows.first
        if window == nil {
            print("ios_wrapper: unable to get key window from shared application\n")
            return nil
        }
        return window!.rootViewController
    }
    
}



var pythonMain: PythonMain?

@_cdecl("SDL_main")
func main(_ argc: Int32, _ argv: UnsafeMutablePointer<UnsafeMutablePointer<CChar>?>) -> Int {
    pythonMain = PythonMain.shared
    run_main(argc, argv)
    //run_python(argc: Int(argc), argv: argv)
    
    return 1
}
