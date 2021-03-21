import React from "react";
import {Card, Col, Row} from 'antd';
import PopupImage from "../PopupImage/PopupImage";
import img from "./../PopupImage/stop.png";

function ImageRow(){
	return(
		<div className="class-carousel">
			<Row gutter={6}>
				<Col>
					<Card>
						Stop Sign
					</Card>
				</Col>
				<Col>
					<PopupImage source={img} />
				</Col>
				<Col>
					<PopupImage source={img} />
				</Col>
				<Col >
					<PopupImage source={img} />
				</Col>
			</Row>
		</div>
	);
}

export default ImageRow;
