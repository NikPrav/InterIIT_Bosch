import React, {useState} from "react";
import {Card, Col, Row, Upload, Button} from "antd";
import PopupImage from "../PopupImage/PopupImage";
import img from "./../PopupImage/stop.png";
import {FaUpload} from "react-icons/fa";
import "./styles.css";

function ImageRow(props) {
  //const img=props.source;
  //console.log(src);
  const [filesList, setfilesList] = useState([{}]);
  const onChange = newfileList => {
    /*
      setfilesList([...filesList,newfileList]);
    */
  };
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
          <Card style={{height: 90}}>Stop Sign</Card>
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
