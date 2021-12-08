// SPDX-License-Identifier: MIT

pragma solidity 0.6.0;

contract Storage {
    uint256 public specialNumber;

    struct People {
        uint256 _favoriteNo;
        string _favoriteName;
    }

    People[] public people;
    mapping(string => uint256) public nameToNumber;

    function store(uint256 _favoriteNumber) public {
        specialNumber = _favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return specialNumber;
    }

    function addPerson(string memory _favoriteName, uint256 _favoriteNo)
        public
    {
        people.push(People(_favoriteNo, _favoriteName));
        nameToNumber[_favoriteName] = _favoriteNo;
    }
}
