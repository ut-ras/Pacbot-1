protobuf:
	protoc --python_out=. ./messages/lightState.proto
	protoc --python_out=. ./messages/pacmanState.proto
	protoc --python_out=. ./messages/subscribe.proto
	protoc --python_out=. ./messages/hardware.proto
	protoc --python_out=. ./messages/gameMode.proto
