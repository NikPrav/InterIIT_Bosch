import React, {useState} from "react";
import {Card, Col, Row, Upload, Button} from "antd";
import PopupImage from "../PopupImage/PopupImage";
import img from "./../PopupImage/stop.png";
import {FaUpload} from "react-icons/fa";
import "./styles.css";
import { UploadOutlined } from '@ant-design/icons';
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
      onSuccess(file)
      console.log(`response:${res}`)
      console.log(res)
    } catch (e) {
      console.log(`Error:${e.message}`);
    }
    }

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
            {/* <Upload style={{height: 90}} accept=".jpg,.jpeg,.png,.webp" fileList={[]}>
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
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default ImageRow;
