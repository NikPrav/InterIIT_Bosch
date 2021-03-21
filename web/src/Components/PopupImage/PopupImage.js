import React, {useState} from "react";
import {Card, Modal, Button, Image} from "antd";
import img from "./stop.png";

function PopupImage(props) {
  const source = props.source;
  const {Meta} = Card;
  const [isModalVisible, setisModalVisible] = useState(false);
  const showModal = () => {
    setisModalVisible(true);
  };

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
          <Image style={{maxHeight: 600}} src={img} />
          <Card title="Metadata" height={600}>
            <p>Metadata</p>
          </Card>
        </div>
      </Modal>
    </div>
  );
}

export default PopupImage;
