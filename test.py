import asyncio
import cv2
import numpy as np
from aiortc import RTCPeerConnection, RTCSessionDescription
from av import VideoFrame
from datetime import datetime, timedelta
import aiohttp

class VideoReceiver:
    def __init__(self):
        self.track = None

    async def handle_track(self, track):
        print("Inside handle track")
        self.track = track
        frame_count = 0
        while True:
            try:
                print("Waiting for frame...")
                frame = await asyncio.wait_for(track.recv(), timeout=5.0)
                frame_count += 1
                print(f"Received frame {frame_count}")
                
                if isinstance(frame, VideoFrame):
                    print(f"Frame type: VideoFrame, pts: {frame.pts}, time_base: {frame.time_base}")
                    frame = frame.to_ndarray(format="bgr24")
                elif isinstance(frame, np.ndarray):
                    print(f"Frame type: numpy array")
                else:
                    print(f"Unexpected frame type: {type(frame)}")
                    continue
              
                # Add timestamp to the frame
                current_time = datetime.now()
                new_time = current_time - timedelta(seconds=55)
                timestamp = new_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                cv2.putText(frame, timestamp, (10, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.imwrite(f"imgs/received_frame_{frame_count}.jpg", frame)
                print(f"Saved frame {frame_count} to file")
                cv2.imshow("Frame", frame)
    
                # Exit on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except asyncio.TimeoutError:
                print("Timeout waiting for frame, continuing...")
            except Exception as e:
                print(f"Error in handle_track: {str(e)}")
                if "Connection" in str(e):
                    break
        print("Exiting handle_track")

async def run(pc, camera_ip, stream_path):
    @pc.on("track")
    def on_track(track):
        print(f"Receiving {track.kind} track")
        asyncio.ensure_future(video_receiver.handle_track(track))

    @pc.on("datachannel")
    def on_datachannel(channel):
        print(f"Data channel established: {channel.label}")

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print(f"Connection state is {pc.connectionState}")
        if pc.connectionState == "connected":
            print("WebRTC connection established successfully")

    # Add transceivers (like in the HTML)
    pc.addTransceiver("audio", direction="recvonly")
    pc.addTransceiver("video", direction="recvonly")

    # Create offer
    print("Creating offer...")
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    print("Local description set")

    # Send offer to camera via HTTP
    url = f"http://{camera_ip}{stream_path}"
    print(f"Sending offer to {url}")
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            headers={"Content-Type": "application/sdp"},
            data=offer.sdp
        ) as response:
            if response.status == 200:
                answer_data = await response.json()
                print("Received answer from camera")
                
                # Set remote description with the answer
                answer = RTCSessionDescription(sdp=answer_data["sdp"], type="answer")
                await pc.setRemoteDescription(answer)
                print("Remote description set")
            else:
                print(f"Error: HTTP {response.status}")
                return

    print("Waiting for connection to be established...")
    while pc.connectionState != "connected" and pc.connectionState != "failed":
        await asyncio.sleep(0.1)

    if pc.connectionState == "failed":
        print("Connection failed!")
        return

    print("Connection established, waiting for frames...")
    await asyncio.sleep(100)  # Wait for frames

    print("Closing connection")

async def main():
    # Use the same camera IP and stream path as in your HTML
    camera_ip = "192.168.20.200:30080"
    stream_path = "/index/api/webrtc?app=live&stream=stream1&type=play"
    
    pc = RTCPeerConnection()
    
    global video_receiver
    video_receiver = VideoReceiver()

    try:
        await run(pc, camera_ip, stream_path)
    except Exception as e:
        print(f"Error in main: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        print("Closing peer connection")
        await pc.close()

if __name__ == "__main__":
    asyncio.run(main())