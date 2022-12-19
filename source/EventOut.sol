pragma solidity 0.8.1;

contract EventOut{
    function eventOut(uint32 _type,bytes memory _value) external override {
        emit OutEvent(msg.sender,_type,_value);
    }
}