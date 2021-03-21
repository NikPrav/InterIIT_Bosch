import React, {useState} from "react";
import {Card, Modal, Button, Image, Radio} from "antd";
import img from "./stop.png";

function PopupImage(props) {
  const source = props.source;
  const {Meta} = Card;
  const [isModalVisible, setisModalVisible] = useState(false);
  const [ImageType, setImageType] = useState('dc')
  const showModal = () => {
    setisModalVisible(true);
  };

  const handleTypeofImage = e => {
    // setImageType(ImageType)
    console.log('radio checked', e.target.value);
    setImageType(e.target.value);
  }

  const handleOk = () => {
    setisModalVisible(false);
  };

  const handleCancel = () => {
    setisModalVisible(false);
  };
  return (
    <div>
      <Card
        onClick={showModal}
        hoverable
        style={{maxWidth: 180}}
        cover={<img alt="example" src={source} maxHeight={50} />}
      ></Card>
      <Modal
        title="Image Properties"
        visible={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        <div style={{display: "flex", flexDir: "row"}}>
          <Image style={{maxHeight: 600 }} src={img} />
          <Card title="Metadata" style = {{height:300,width:500}}>
            <p>Training Preference</p>
            <Radio.Group onChange={handleTypeofImage} value={ImageType}>
              <Radio value={'train'}>Train</Radio>
              <Radio value={'test'}>Test</Radio>
              <Radio value={'dc'}>Don't Care</Radio>
            </Radio.Group>
          </Card>
        </div>
      </Modal>
    </div>
  );
}

export default PopupImage;
