# Using Apple API part 1







add 

```swift
import UIKit
```

to the top of the PythonMain.swift file

and then add the following var to the PythonMain class

```swift
var viewcontroller: UIViewController?
```

now lets make another extension to the PythonMain class

```swift
extension PythonMain {
    
}
```

and add the following function to the extension:

```swift
func get_viewcontroller() -> UIViewController? {
    let window = UIApplication.shared.windows.first
    if window == nil {
        print("ios_wrapper: unable to get key window from shared application\n")
        return nil
    }
    return window!.rootViewController
}
```

```swift
func openFiles(){
    let documentPicker = UIDocumentPickerViewController(documentTypes: [], in: .open)
    self.viewcontroller.present(documentPicker, animated: true, completion: nil)
}
```

```swift
func viewPDF(){
    let presentVC = UIViewController()
    let pdfView = PDFView(frame: presentVC.view.bounds)
    presentVC.view = pdfView

    self.viewcontroller.present(presentVC, animated: true, completion: nil)
    let fileURL = Bundle.main.url(forResource: "kivy", withExtension: "pdf")
    pdfView.document = PDFDocument(url: fileURL!)
}
```

