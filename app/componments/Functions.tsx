import React from 'react';
import {
  ScrollView,
  TouchableOpacity,
  Text,
  StyleSheet,
  View,
} from 'react-native';

type ButtonOption = {
  id: string;
  label: string;
};
const options = [
  {id: '1', label: '文本扫描OCR'},
  {id: '2', label: '证件照片制作'},
  {id: '3', label: '文件格式转换'},
  {id: '4', label: '水印'},
  // ... 更多选项
];

export default function ScrollableButtonSelector({handleSelect}) {
  return (
    <ScrollView
      horizontal
      showsHorizontalScrollIndicator={false}
      style={styles.scrollView}>
      {options.map(option => (
        <TouchableOpacity
          key={option.id}
          style={styles.button}
          onPress={() => handleSelect(option.label)}>
          <Text style={styles.buttonText}>{option.label}</Text>
          <Text style={[styles.buttonText, {color: 'grey'}]}>icon</Text>
        </TouchableOpacity>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  scrollView: {
    flexDirection: 'row',
  },
  button: {
    width: 150,
    height: 100,
    margin: 5,
    paddingVertical: 8,
    paddingHorizontal: 16,
    backgroundColor: '#444444',
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.22,
    shadowRadius: 2.22,
    elevation: 3,
  },
  buttonText: {
    fontSize: 16,
    color: 'white',
  },
});
