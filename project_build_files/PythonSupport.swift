//
//  PythonSupport.swift
//  kivy_swifttest
//
//  Created by macdaw on 01/04/2021.
//

import Foundation


func pointer2array<T>(data: UnsafePointer<T>,count: Int) -> [T] {

    let buffer = UnsafeBufferPointer(start: data, count: count);
    return Array<T>(buffer)
}

extension UnsafePointer where Pointee == Int8 {
    func asString() -> String {
        return String(cString: self )
    }
}
