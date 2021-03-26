import React, {useState} from "react";
import {Card, Col, Row, Upload, Button,message} from "antd";
import PopupImage from "../PopupImage/PopupImage";
import img from "./../PopupImage/stop.png";
import {FaUpload} from "react-icons/fa";
import { UploadOutlined } from '@ant-design/icons';

import "./styles.css";
import axios from 'axios'
import request from "umi-request";

function ImageRow(props) {
  //const img=props.source;
  //console.log(src);
  const [filesList, setfilesList] = useState([{}]);
  const onChange = newfileList => {
    /*
      setfilesList([...filesList,newfileList]);
    */
  };
  // const imageStuff = {
  //   action: 'https://www.mocky.io/v2/5cc8019d300000980a055e76',
    
  //   onChange(info) {
  //     if (info.file.status !== 'uploading') {
  //       console.log(info.file, info.fileList);
  //     }
  //     if (info.file.status === 'done') {
  //       message.success(`${info.file.name} file uploaded successfully`);
  //     } else if (info.file.status === 'error') {
  //       message.error(`${info.file.name} file upload failed.`);
  //     }
  //   },
  // };
  const handleOnChange = ({ file, fileList, event }) => {
    console.log(file, fileList, event);
    //Using Hooks to update the state to the current filelist
    // setDefaultFileList(fileList);
    //filelist - [{uid: "-1",url:'Some url to image'}]
  };
  const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });

  const uploadImage = async options => {

    const { onSuccess, onError, file, onProgress } = options;
    console.log(`X:${file}`)
    console.log(file)
    
    // const fmData = new FormData();
    // const fmData = {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ image: file })
    // }; 
    // const config = {
    //   // headers: { "content-type": "multipart/form-data" },
    //   onUploadProgress: event => {
    //     console.log((event.loaded / event.total) * 100);
    //     onProgress({ percent: (event.loaded / event.total) * 100 },file);
    //   }
    // };
    // const requestOptions = {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ image: file })
    // };
    // fmData.append("image", file);
    try{
        
      const base64data = await toBase64(file);
      
      console.log(base64data);
      // console.log(atob(base64data))/
   
      const UrlToSendDataTo = 'http://localhost:5000/pictest'
      const response = await request(UrlToSendDataTo, {
        method: "post",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: base64data })
      });
      const res = response
      console.log(`response:${res}`)
      console.log(res)
      // const requestOptions = {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ image: base64data })
      // };
      // const response = await fetch('http://localhost:5000/pictest', requestOptions)
      //   // .then(response => response.text())
      // const res = response
      // console.log(response)
    } catch (e) {
      console.log(`Error:${e.message}`);
    }
    }
  //   axios
  //     .post("http://localhost:5000/pictest", fmData, config)
  //     .then(res => {
  //       onSuccess(file);
  //       console.log(res);
  //     })
  //     .catch(err=>{
  //       const error = new Error('Some error');
  //       onError({event:error});
  //     });
  // }
  
  

  const DataClass = props.DataClass;
  console.log(filesList);
  return (
    <div className="class-carousel">
      <Row
        gutter={6}
        style={{
          height: "120px",
          width: "100%",
          whiteSpace: "nowrap",
          overflowX: "scroll",
          flexWrap: "nowrap",
        }}
      >
        <Col style={{height: "100px", minWidth: "90px"}}>
          <Card style={{height: 90}}>
            {DataClass}
            <br />
            {/* <Upload>
              <Button>
                <FaUpload />
              </Button>
            </Upload> */}
            <Upload 
            // {...imageStuff}
            // accept="image/*"
            customRequest={uploadImage}
            onChange={handleOnChange}

            >
              <Button icon={<UploadOutlined />}>Click to Upload</Button>
            </Upload>,
            {/* <div>
                <input type="file" onChange={onFileChange} />
                <button onClick={onFileUpload}>
                  Upload!
                </button>
            </div>
            <div>
            {/* {fileData()} 
            </div> */}
          </Card>
        </Col>
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>

        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>

        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>

        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>

        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>

        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>

        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>

        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        <Col style={{minWidth: "90px"}}>
          <PopupImage source={img} />
        </Col>
        {filesList.map(file => {
          <PopupImage source={file} />;
        })}
        <Col>
          <Card style={{height: 90}}>
            <Upload style={{height: 90}} accept=".jpg,.jpeg,.png,.webp" fileList={[]}>
              <Button>
                <FaUpload />
              </Button>
            </Upload>
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default ImageRow;
