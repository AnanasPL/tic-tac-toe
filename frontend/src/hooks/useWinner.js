import { useContext, useEffect, useState } from 'react'
import { modalVisibleContext } from '../contexts/modalContext'

const useWinner = () => {
  const [winner, setWinner] = useState(null)
  const [playerSymbol, setPlayerSymbol] = useState('')

  const setModalVisible = useContext(modalVisibleContext)

  useEffect(() => {
    if (!winner) {
      setModalVisible(false)
    }

    setModalVisible()
  }, [winner])
}

export default useWinner
