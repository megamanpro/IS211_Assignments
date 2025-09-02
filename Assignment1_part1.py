{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "eb996a39-ce45-43db-a596-3a9809d02e01",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "test_list_divide passed successfully\n"
     ]
    }
   ],
   "source": [
    "class ListDivideException(Exception):\n",
    "    pass\n",
    "\n",
    "def list_divide(numbers, divide=2):\n",
    "    count = 0\n",
    "    for n in numbers:\n",
    "        if n % divide == 0:\n",
    "            count += 1\n",
    "    return count\n",
    "\n",
    "def test_list_divide():\n",
    "\n",
    "    try:\n",
    "        assert list_divide([1, 2, 3, 4, 5]) == 2\n",
    "        assert list_divide([2, 4, 6, 8, 10]) == 5\n",
    "        assert list_divide([30, 54, 63, 98, 100], divide=10) == 2\n",
    "        assert list_divide([]) == 0\n",
    "        assert list_divide([1, 2, 3, 4, 5], 1) == 5\n",
    "    except AssertionError:\n",
    "        raise ListDivideException(\"list_divide failed one or more tests\")\n",
    "    else:\n",
    "        print(\"test_list_divide passed successfully\")\n",
    "\n",
    "test_list_divide()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "beba32ca-dc0c-43f3-89e7-9f1a2ceda4f0",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
